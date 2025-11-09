# src/validators/email_validator.py
from email_validator import validate_email as ev_validate, EmailNotValidError
import re
from typing import Iterable, Optional
from ._types import ValidationResult

# Defaults; puedes externalizar a config/settings.py
MAX_EMAIL_LENGTH = 254
MAX_LOCALPART = 64
DOMAIN_BLOCKLIST = {
    "tempmail.com",
    "10minutemail.com",
    "mailinator.com",
    "disposablemail.com",
}

# regex para TLD: al menos 2 letras, no solo numeros
_TLD_RE = re.compile(r"^[A-Za-z]{2,}$")

# regex para detectar consecutive dots or leading/trailing dot in local part
_CONSECUTIVE_DOTS_RE = re.compile(r"\.\.")
_LEADING_TRAILING_DOT_RE = re.compile(r"(^\.|\.$)")

def _check_tld(tld: str) -> bool:
    # devuelve True si el tld parece razonable (solo letras, largo >=2)
    return bool(_TLD_RE.match(tld))

def validate_email(email: str,
                   domain_blocklist: Optional[Iterable[str]] = None,
                   check_deliverability: bool = False
                   ) -> ValidationResult:
    """
    Validacion estrica de email:
    - usa email_validator para parsing RFC-syntactic
    - aplica checks adicionales: longitudes, puntos consecutivos, tld razonable, blocklist
    - param check_deliverability: pasa check_deliverability a email_validator.validate_email
    """
    email_in = (email or "").strip()
    if not email_in:
        return ValidationResult(False, "lexical", ["Entrada vacía"], None)

    # Lexical check: caracteres imprimibles básicos (no control chars)
    if any(ord(c) < 32 for c in email_in):
        return ValidationResult(False, "lexical", ["Caracteres no imprimibles en el correo"], None)

    # basic length fast-fail
    if len(email_in) > MAX_EMAIL_LENGTH:
        return ValidationResult(False, "syntactic", [f"Email excede longitud máxima ({MAX_EMAIL_LENGTH})"], None)

    try:
        r = ev_validate(email_in, check_deliverability=check_deliverability)
    except EmailNotValidError as e:
        # email_validator da mensajes legibles según RFC
        return ValidationResult(False, "syntactic", [str(e)], None)

    norm = r.normalized  # normalizado (minusculas en dominio, punycode si aplica)
    
    if norm is None:
        return ValidationResult(False, "syntactic", ["No se pudo normalizar el email"], None)

    # semantic checks
    local_part, domain = norm.rsplit("@", 1)

    # local part length
    if len(local_part) > MAX_LOCALPART:
        return ValidationResult(False, "semantic", [f"Local part excede {MAX_LOCALPART} caracteres"], norm)

    # no leading/trailing dot in local part
    if _LEADING_TRAILING_DOT_RE.search(local_part):
        return ValidationResult(False, "syntactic", ["Punto al inicio o final del local part"], norm)

    # no consecutive dots in local part
    if _CONSECUTIVE_DOTS_RE.search(local_part):
        return ValidationResult(False, "syntactic", ["Secuencia de puntos consecutivos en local part"], norm)

    # Domain / TLD checks
    if domain.lower() in (d.lower() for d in (domain_blocklist or DOMAIN_BLOCKLIST)):
        return ValidationResult(False, "semantic", ["Dominio en lista negra (disposable/temporal)"], norm)

    # split tld candidate - take last label after last dot
    if "." not in domain:
        return ValidationResult(False, "syntactic", ["Dominio sin TLD"], norm)
    tld = domain.rsplit(".", 1)[1]
    if not _check_tld(tld):
        return ValidationResult(False, "semantic", [f"TLD no válido o poco común: '{tld}'"], norm)

    # no numeric-only TLD (e.g., ".123" is invalid)
    if tld.isdigit():
        return ValidationResult(False, "semantic", ["TLD no puede ser solo números"], norm)

    return ValidationResult(True, "semantic", [], norm)

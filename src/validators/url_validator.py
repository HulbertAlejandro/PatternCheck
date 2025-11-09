# src/validators/url_validator.py
import re
from urllib.parse import urlparse
from ._types import ValidationResult

URL_RE = re.compile(
    r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", re.IGNORECASE
)

def validate_url(url: str, require_https: bool = False) -> ValidationResult:
    if not url or not url.strip():
        return ValidationResult(False, "lexical", ["URL vacía"], None)

    s = url.strip()

    if not URL_RE.match(s):
        return ValidationResult(False, "syntactic", ["Formato de URL inválido"], None)

    parsed = urlparse(s)
    if require_https and parsed.scheme.lower() != "https":
        return ValidationResult(False, "semantic", ["Se requiere HTTPS"], None)

    # Semántica mínima: debe tener dominio
    if not parsed.netloc or "." not in parsed.netloc:
        return ValidationResult(False, "semantic", ["Dominio inválido o ausente"], None)

    # Normalizar
    norm = parsed.geturl().rstrip("/")

    return ValidationResult(True, "semantic", ["URL válida"], norm)

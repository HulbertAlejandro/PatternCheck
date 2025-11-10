# src/validators/postal_validator.py
import re
from typing import Optional
from ._types import ValidationResult

# ---------- Reglas de códigos postales por país ----------
POSTAL_RULES = {
    "CO": r"^\d{6}$",                        # Colombia: 6 dígitos
    "US": r"^\d{5}(?:-\d{4})?$",             # EE.UU.: ZIP o ZIP+4
    "ES": r"^(?:0[1-9]|[1-4]\d|5[0-2])\d{3}$", # España: 01000–52999
    "MX": r"^\d{5}$",                        # México: 5 dígitos
    "AR": r"^[A-Z]\d{4}[A-Z]{3}$",           # Argentina: CPA (A1234ABC)
}

# Países donde se deben eliminar espacios o guiones antes de validar
NORMALIZE_REMOVE = {"US", "AR"}


# ---------- Normalización ----------
def _normalize_postal_input(postal: str, country: str) -> str:
    """Normaliza el código postal (quita espacios y guiones según país)."""
    p = (postal or "").strip().upper()
    if country in NORMALIZE_REMOVE:
        p = re.sub(r"[\s\-]", "", p)
    return p


# ---------- Detección automática del país ----------
def _detect_country(postal: str) -> Optional[str]:
    """
    Intenta inferir el país basándose en los patrones conocidos.
    Devuelve el código ISO del país o None si no se detecta.
    """
    normalized = re.sub(r"[\s\-]", "", (postal or "").strip().upper())
    for code, pattern in POSTAL_RULES.items():
        if re.fullmatch(pattern, normalized):
            return code
    return None


# ---------- Validadores específicos ----------
def validate_co(postal_norm: str) -> bool:
    return bool(re.fullmatch(POSTAL_RULES["CO"], postal_norm))

def validate_us(postal_norm: str) -> bool:
    return bool(re.fullmatch(POSTAL_RULES["US"], postal_norm))

def validate_es(postal_norm: str) -> bool:
    return bool(re.fullmatch(POSTAL_RULES["ES"], postal_norm))

def validate_mx(postal_norm: str) -> bool:
    return bool(re.fullmatch(POSTAL_RULES["MX"], postal_norm))

def validate_ar(postal_norm: str) -> bool:
    return bool(re.fullmatch(POSTAL_RULES["AR"], postal_norm))


# ---------- Dispatcher principal ----------
def validate_postal(postal: str, country: Optional[str] = None, debug: bool = False) -> ValidationResult:
    """
    Valida un código postal según el país.
    Si no se indica país, se intenta detectar automáticamente.
    """
    if not postal or not postal.strip():
        return ValidationResult(False, "lexical", ["Código postal vacío"], None)

    original = postal.strip().upper()
    country = (country or "").strip().upper()

    # Si no se pasa el país, intentar detectarlo automáticamente
    if not country:
        detected = _detect_country(original)
        if detected:
            country = detected
            if debug:
                print(f"País detectado automáticamente: {country}")
        else:
            return ValidationResult(False, "semantic", ["No se pudo determinar el país del código postal"], None)

    if country not in POSTAL_RULES:
        return ValidationResult(False, "semantic", [f"País no soportado: {country}"], None)

    # Normalizar el input
    p = _normalize_postal_input(original, country)
    pattern = POSTAL_RULES[country]

    if debug:
        print(f"Validando postal: {original} | País: {country} | Normalizado: {p} | Patrón: {pattern}")

    # Seleccionar validador por país
    validators = {
        "CO": validate_co,
        "US": validate_us,
        "ES": validate_es,
        "MX": validate_mx,
        "AR": validate_ar,
    }
    valid = validators[country](p)

    if not valid:
        msg = f"Código postal inválido para {country}"
        if debug:
            msg += f" (normalizado={p}, patrón={pattern})"
        return ValidationResult(False, "syntactic", [msg], None)

    return ValidationResult(True, "semantic", [f"Código postal válido ({country})"], p)


# ---------- Pruebas manuales ----------
if __name__ == "__main__":
    tests = [
        ("110111", None),        # ✅ Colombia
        ("90210", None),         # ✅ USA (ZIP)
        ("90210-1234", None),    # ✅ USA (ZIP+4)
        ("28013", None),         # ✅ España (Madrid)
        ("52999", None),         # ✅ España (máximo permitido)
        ("12345", None),         # ✅ México
        ("A1000ABC", None),      # ✅ Argentina
        ("a1000abc", None),      # ✅ Argentina (minúsculas -> normaliza)
        ("123", None),           # ❌ Inválido
        ("", None),              # ❌ Vacío
    ]

    for postal, country in tests:
        res = validate_postal(postal, country, debug=True)
        print(f"{postal} ({country}) -> valid={res.valid}, msgs={res.messages}, valor={res.value}\n")

# src/validators/id_validator.py
import re
from ._types import ValidationResult

# patrones simples por país
COUNTRY_ID_RULES = {
    "CO": {"min_len": 7, "max_len": 10, "pattern": r"^\d{7,10}$"},
    "US": {"min_len": 9, "max_len": 9, "pattern": r"^\d{9}$"},
    "MX": {"min_len": 10, "max_len": 18, "pattern": r"^[A-Z0-9]{10,18}$"},
}

TRIVIAL_PATTERNS = {"0000000", "1111111", "1234567", "9876543"}

def validate_id(id_str: str, country: str = "CO") -> ValidationResult:
    if not id_str or not id_str.strip():
        return ValidationResult(False, "lexical", ["Identificación vacía"], None)

    s = id_str.strip()
    rule = COUNTRY_ID_RULES.get(country.upper(), COUNTRY_ID_RULES["CO"])

    # léxico
    if not re.match(rule["pattern"], s):
        return ValidationResult(False, "syntactic", [f"Formato inválido para {country.upper()}"], None)

    # semántica
    if s in TRIVIAL_PATTERNS:
        return ValidationResult(False, "semantic", ["Identificación trivial o secuencial"], None)

    if not (rule["min_len"] <= len(s) <= rule["max_len"]):
        return ValidationResult(False, "semantic", ["Longitud fuera de rango"], None)

    return ValidationResult(True, "semantic", ["Identificación válida"], s)

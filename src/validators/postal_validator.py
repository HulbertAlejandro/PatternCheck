# src/validators/postal_validator.py
import re
from ._types import ValidationResult

COUNTRY_POSTAL_RULES = {
    "CO": r"^\d{6}$",
    "US": r"^\d{5}(-\d{4})?$",
    "ES": r"^(?:0[1-9]|[1-4]\d|5[0-2])\d{3}$",
    "MX": r"^\d{5}$",
    "AR": r"^[A-Z]\d{4}[A-Z]{3}$",
}

def validate_postal(postal: str, country: str = "CO") -> ValidationResult:
    if not postal or not postal.strip():
        return ValidationResult(False, "lexical", ["Código postal vacío"], None)

    p = postal.strip()
    pattern = COUNTRY_POSTAL_RULES.get(country.upper())

    if not pattern:
        return ValidationResult(False, "semantic", [f"No hay reglas definidas para {country.upper()}"], None)

    if not re.match(pattern, p):
        return ValidationResult(False, "syntactic", [f"Código postal inválido para {country.upper()}"], None)

    return ValidationResult(True, "semantic", ["Código postal válido"], p)

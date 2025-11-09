# src/validators/plate_validator.py
import re
from ._types import ValidationResult

PLATE_RULES = {
    "CO": r"^[A-Z]{3}-?\d{3}$",
    "MX": r"^[A-Z]{3}-\d{3,4}$",
    "US": r"^[A-Z0-9]{1,7}$",
    "AR": r"^[A-Z]{2}\d{3}[A-Z]{2}$",
}

def validate_plate(plate: str, country: str = "CO") -> ValidationResult:
    if not plate or not plate.strip():
        return ValidationResult(False, "lexical", ["Placa vacía"], None)

    p = plate.strip().upper()
    pattern = PLATE_RULES.get(country.upper(), PLATE_RULES["CO"])

    if not re.match(pattern, p):
        return ValidationResult(False, "syntactic", [f"Formato de placa inválido para {country.upper()}"], None)

    return ValidationResult(True, "semantic", ["Placa válida"], p)

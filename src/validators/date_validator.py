# src/validators/date_validator.py
from datetime import datetime, date
from dateutil import parser
from ._types import ValidationResult

VALID_FORMATS = [
    "%Y-%m-%d",  # ISO
    "%d/%m/%Y",  # formato común en LatAm
    "%m/%d/%Y",  # formato US
    "%d-%m-%Y",
]

def _parse_date_custom(date_str: str, dayfirst: bool = True) -> datetime:
    """Intenta parsear usando dateutil con control de dayfirst."""
    return parser.parse(date_str, dayfirst=dayfirst)

def validate_date(date_str: str, region: str = "CO", allow_future: bool = True) -> ValidationResult:
    """
    Valida formato y semántica de fechas.
    - region: para decidir dayfirst (True en CO, ES, MX)
    - allow_future: si False, fechas futuras son inválidas
    """
    if not date_str or not date_str.strip():
        return ValidationResult(False, "lexical", ["Entrada vacía"], None)
    
    s = date_str.strip()
    dayfirst = region.upper() in ("CO", "ES", "MX", "AR", "PE", "CL")

    try:
        dt = _parse_date_custom(s, dayfirst=dayfirst)
    except Exception:
        return ValidationResult(False, "syntactic", ["Formato de fecha inválido"], None)

    # Semántica: no permitir fechas imposibles (datetime ya lo controla)
    # Revisar año rango razonable
    if dt.year < 1900 or dt.year > 2100:
        return ValidationResult(False, "semantic", [f"Año fuera de rango razonable: {dt.year}"], None)

    # No permitir fechas futuras si no se autoriza
    today = date.today()
    if not allow_future and dt.date() > today:
        return ValidationResult(False, "semantic", ["No se permiten fechas futuras"], dt.strftime("%Y-%m-%d"))

    return ValidationResult(True, "semantic", ["Fecha válida"], dt.strftime("%Y-%m-%d"))

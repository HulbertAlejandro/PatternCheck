import re
from ._types import ValidationResult
from typing import Optional

# ---------- Patrones por país ----------
PLATE_RULES = {
    "CO": r"^(?:[A-Z]{3}\d{3}|[A-Z]{3}\d{2}[A-Z])$",       # CO: carro o moto
    "MX": r"^[A-Z]{3}\d{3,4}$",                            # MX: ABC123 o ABC1234
    "US": r"^[A-Z0-9]{1,7}$",                              # US: 1-7 alfanuméricos
    "AR": r"^(?:[A-Z]{2}\d{3}[A-Z]{2}|[A-Z]{3}\d{3})$",    # AR: AA123BB o ABC123
}

# Países a los que se les remueven espacios/guiones antes de validar
NORMALIZE_REMOVE = {"MX", "US", "AR"}


# ---------- Normalización ----------
def _normalize_plate_input(plate: str, country: str) -> str:
    p = (plate or "").strip().upper()
    if country in NORMALIZE_REMOVE:
        p = re.sub(r"[\s\-]", "", p)
    return p


# ---------- Detectar país automáticamente ----------
def _detect_country(plate: str) -> Optional[str]:
    """
    Intenta inferir el país basándose en los patrones conocidos.
    Devuelve el código ISO o None si no se detecta.
    """
    normalized = re.sub(r"[\s\-]", "", (plate or "").strip().upper())
    for code, pattern in PLATE_RULES.items():
        if re.fullmatch(pattern, normalized):
            return code
    return None


# ---------- Validadores específicos ----------
def validate_co(plate_norm: str) -> bool:
    return bool(re.fullmatch(PLATE_RULES["CO"], plate_norm))

def validate_mx(plate_norm: str) -> bool:
    return bool(re.fullmatch(PLATE_RULES["MX"], plate_norm))

def validate_us(plate_norm: str) -> bool:
    return bool(re.fullmatch(PLATE_RULES["US"], plate_norm))

def validate_ar(plate_norm: str) -> bool:
    return bool(re.fullmatch(PLATE_RULES["AR"], plate_norm))


# ---------- Dispatcher principal ----------
def validate_plate(plate: str, country: Optional[str] = None, debug: bool = False) -> ValidationResult:
    """
    Valida una placa según país. Si el país no se pasa, intenta detectarlo automáticamente.
    """
    if not plate or not plate.strip():
        return ValidationResult(False, "lexical", ["Placa vacía"], None)

    original = plate.strip().upper()

    # Si no se especifica país, detectarlo automáticamente
    country = (country or "").strip().upper()
    if not country:
        detected = _detect_country(original)
        if detected:
            country = detected
            if debug:
                print(f"País detectado automáticamente: {country}")
        else:
            return ValidationResult(False, "semantic", ["No se pudo determinar el país de la placa"], None)

    if country not in PLATE_RULES:
        return ValidationResult(False, "semantic", [f"País no soportado: {country}"], None)

    # Normalizar entrada
    p = _normalize_plate_input(original, country)
    pattern = PLATE_RULES[country]

    if debug:
        print(f"Validando placa: {original} | País: {country} | Normalizada: {p}")

    # Elegir validador por país
    validators = {
        "CO": validate_co,
        "MX": validate_mx,
        "US": validate_us,
        "AR": validate_ar,
    }
    valid = validators[country](p)

    if not valid:
        msg = f"Formato de placa inválido para {country}"
        if debug:
            msg += f" (normalizada={p}, patrón={pattern})"
        return ValidationResult(False, "syntactic", [msg], None)

    return ValidationResult(True, "semantic", [f"Placa válida ({country})"], p)


# ---------- Pruebas manuales ----------
if __name__ == "__main__":
    tests = [
        ("TBR123", None),      # Detecta CO
        ("TBR12G", None),      # Detecta CO (moto)
        ("ABC-123", None),     # Detecta MX
        ("ABC 1234", None),    # Detecta MX
        ("7ABC234", None),     # Detecta US
        ("A B -1 23", None),   # Detecta US
        ("AB123CD", None),     # Detecta AR
        ("ABC-123", None),     # Detecta AR (viejo)
        ("XYZ999", None),      # Detecta CO
        ("abc 1234", None),    # Detecta MX
        ("7abc234", None),     # Detecta US
    ]

    for plate, country in tests:
        res = validate_plate(plate, country, debug=True)
        print(f"{plate} ({country}) -> valid={res.valid}, msgs={res.messages}, valor={res.value}\n")

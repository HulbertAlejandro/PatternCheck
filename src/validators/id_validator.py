# src/validators/id_validator.py
import re
from typing import Optional
from ._types import ValidationResult

# ---------- Reglas de identificación por país ----------
ID_RULES = {
    # Colombia: cédula de 7 a 10 dígitos
    "CO": r"^\d{7,10}$",

    # Estados Unidos: SSN (9 dígitos, con o sin guiones)
    "US": r"^\d{3}-?\d{2}-?\d{4}$",

    # México: CURP (18) o RFC (13)
    "MX": r"^(?:[A-Z]{4}\d{6}[HM][A-Z]{5}\d{2}|[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3})$",
}

# Países donde se remueven espacios o guiones antes de validar (NO incluimos "US" para no romper SSN)
NORMALIZE_REMOVE = {"MX"}

# Patrones triviales o secuenciales que deben rechazarse (solo repeticiones obvias)
TRIVIAL_PATTERNS = {"000000000", "111111111", "222222222", "999999999"}


# ---------- Normalización ----------
def _normalize_id_input(id_str: str, country: str) -> str:
    """
    Normaliza la entrada según país.
    - Para MX: elimina espacios y guiones (CURP/RFC no deben tener guiones).
    - Para US: no eliminamos guiones para conservar formato posible "123-45-6789",
      pero al comprobar trivialidad se limpia temporalmente.
    """
    s = (id_str or "").strip().upper()
    if country in NORMALIZE_REMOVE:
        s = re.sub(r"[\s\-]", "", s)
    return s


# ---------- Detección automática ----------
def _detect_country(id_str: str) -> Optional[str]:
    """
    Intenta inferir el país basándose en el formato (prueba original y versión limpia).
    """
    if not id_str:
        return None
    original = id_str.strip().upper()
    cleaned = re.sub(r"[\s\-]", "", original)
    for code, pattern in ID_RULES.items():
        # pruebo con la forma original (útil para US con guiones) y con la limpia
        if re.fullmatch(pattern, original) or re.fullmatch(pattern, cleaned):
            return code
    return None


# ---------- Validadores específicos ----------
def validate_co(id_norm: str) -> bool:
    return bool(re.fullmatch(ID_RULES["CO"], id_norm))

def validate_us(id_norm: str) -> bool:
    # acepta SSN con o sin guiones
    return bool(re.fullmatch(ID_RULES["US"], id_norm))

def validate_mx(id_norm: str) -> bool:
    return bool(re.fullmatch(ID_RULES["MX"], id_norm))


# ---------- Dispatcher principal ----------
def validate_id(id_str: str, country: Optional[str] = None, debug: bool = False) -> ValidationResult:
    """
    Valida una identificación nacional según el país.
    Si no se especifica el país, intenta detectarlo automáticamente.
    """
    if not id_str or not id_str.strip():
        return ValidationResult(False, "lexical", ["Identificación vacía"], None)

    original = id_str.strip()
    country = (country or "").strip().upper()

    # autodetección si no llega country
    if not country:
        detected = _detect_country(original)
        if detected:
            country = detected
            if debug:
                print(f"DEBUG: País detectado automáticamente: {country}")
        else:
            return ValidationResult(False, "semantic", ["No se pudo determinar el país del ID"], None)

    if country not in ID_RULES:
        return ValidationResult(False, "semantic", [f"País no soportado: {country}"], None)

    # normalizar según país
    s = _normalize_id_input(original, country)

    if debug:
        print(f"DEBUG: Validando ID original={original!r}, country={country}, normalizada={s!r}")

    # validar con el validador específico
    validators = {"CO": validate_co, "US": validate_us, "MX": validate_mx}
    valid = validators[country](s)

    # comprobar trivialidad sobre la versión limpia (sin guiones/espacios)
    s_clean = re.sub(r"[\s\-]", "", s)
    if s_clean in TRIVIAL_PATTERNS:
        return ValidationResult(False, "semantic", ["Identificación trivial o secuencial"], None)

    if not valid:
        msg = f"Formato de identificación inválido para {country}"
        if debug:
            msg += f" (normalizada={s}, patrón={ID_RULES[country]})"
        return ValidationResult(False, "syntactic", [msg], None)

    # devolver valor normalizado para almacenamiento (para US devolvemos la versión sin guiones para consistencia)
    # Si quieres mantener guiones en salida, cambia p_return = s en lugar de s_clean.
    p_return = s_clean if country == "US" else s
    return ValidationResult(True, "semantic", [f"Identificación válida ({country})"], p_return)


# ---------- Pruebas manuales ----------
if __name__ == "__main__":
    tests = [
        ("123456789", None),
        ("123-45-6789", None),
        ("123456789", "US"),
        ("123-45-6789", "US"),
        ("1032456789", None),
        ("ABCD900101HDFXYZ01", None),
        ("111111111", None),
    ]

    for id_str, country in tests:
        res = validate_id(id_str, country, debug=True)
        print(f"{id_str!r} ({country}) -> valid={res.valid}, msgs={res.messages}, valor={res.value}")

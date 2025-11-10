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

# Países donde se remueven espacios o guiones antes de validar
NORMALIZE_REMOVE = {"MX"}

# Patrones triviales o secuenciales que deben rechazarse
TRIVIAL_PATTERNS = {"000000000", "111111111", "222222222", "999999999"}


# ---------- Normalización ----------
def _normalize_id_input(id_str: str, country: str) -> str:
    s = (id_str or "").strip().upper()
    if country in NORMALIZE_REMOVE:
        s = re.sub(r"[\s\-]", "", s)
    return s


# ---------- Detección automática ----------
def _detect_country(id_str: str) -> Optional[str]:
    if not id_str:
        return None
    original = id_str.strip().upper()
    cleaned = re.sub(r"[\s\-]", "", original)
    for code, pattern in ID_RULES.items():
        if re.fullmatch(pattern, original) or re.fullmatch(pattern, cleaned):
            return code
    return None


# ---------- Validadores específicos ----------
def _is_sequential(number_str: str) -> bool:
    """Detecta secuencias ascendentes o descendentes (e.g., 1234567 o 9876543)."""
    if len(number_str) < 3 or not number_str.isdigit():
        return False
    asc = "0123456789"
    desc = asc[::-1]
    return number_str in asc or number_str in desc or any(
        number_str in asc[i:] or number_str in desc[i:] for i in range(len(asc))
    )


def validate_co(id_norm: str) -> bool:
    """Valida cédula colombiana (7 a 10 dígitos, sin repeticiones ni secuencias)."""
    if not re.fullmatch(ID_RULES["CO"], id_norm):
        return False
    # No permitir todos los dígitos iguales ni secuencias ascendentes/descendentes
    if len(set(id_norm)) == 1 or _is_sequential(id_norm):
        return False
    return True


def validate_us(id_norm: str) -> bool:
    return bool(re.fullmatch(ID_RULES["US"], id_norm))


def validate_mx(id_norm: str) -> bool:
    return bool(re.fullmatch(ID_RULES["MX"], id_norm))


# ---------- Dispatcher principal ----------
def validate_id(id_str: str, country: Optional[str] = None, debug: bool = False) -> ValidationResult:
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

    p_return = s_clean if country == "US" else s
    return ValidationResult(True, "semantic", [f"Identificación válida ({country})"], p_return)


# ---------- Pruebas manuales ----------
if __name__ == "__main__":
    tests = [
        ("1032456789", "CO"),  # ✅ válida
        ("11111111", "CO"),    # ❌ repetitiva
        ("12345678", "CO"),    # ❌ secuencial
        ("87654321", "CO"),    # ❌ descendente
        ("123-45-6789", "US"), # ✅ válida
        ("ABCD900101HDFXYZ01", "MX"), # ✅ válida
    ]

    for id_str, country in tests:
        res = validate_id(id_str, country, debug=True)
        print(f"{id_str!r} ({country}) -> valid={res.valid}, msgs={res.messages}, valor={res.value}")

from dataclasses import dataclass
from typing import Optional, List
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException, region_code_for_number
from ._types import ValidationResult


# --- CONFIGURACIÓN GENERAL ---
PAISES_ADMITIDOS = ["CO", "MX", "US"]  # Colombia, México, Estados Unidos


@dataclass
class PhoneValidationMeta:
    e164: Optional[str]
    region: Optional[str]
    country_code: Optional[int]
    number_type: Optional[str]
    possible: bool
    valid: bool
    raw_input: str


def _number_type_name(num_type) -> str:
    """Convierte el tipo de número (fijo, móvil, etc.) a texto legible."""
    from phonenumbers import PhoneNumberType
    mapping = {v: k for k, v in PhoneNumberType.__dict__.items() if not k.startswith("_")}
    return mapping.get(num_type, str(num_type))


def validate_phone(raw: str, country_hint: Optional[str] = None) -> ValidationResult:
    """
    Valida y normaliza un número telefónico.
    Acepta números de Colombia (CO), México (MX) y Estados Unidos (US).
    """
    raw_in = (raw or "").strip()
    if not raw_in:
        return ValidationResult(False, "lexical", ["Entrada vacía"], None)

    # Chequeo léxico rápido: caracteres permitidos
    for c in raw_in:
        if not (c.isdigit() or c in "+- ()"):
            return ValidationResult(False, "lexical", [f"Carácter no permitido: '{c}'"], None)

    # --- Intento de parseo ---
    parsed = None
    errores: List[str] = []

    # Si el usuario incluye el prefijo internacional (+)
    if raw_in.startswith("+"):
        try:
            parsed = phonenumbers.parse(raw_in, None)
        except NumberParseException as e:
            errores.append(f"Error al interpretar número internacional: {e}")
    else:
        # Intentar con los países admitidos
        for pais in PAISES_ADMITIDOS:
            try:
                parsed = phonenumbers.parse(raw_in, pais)
                if phonenumbers.is_possible_number(parsed):
                    break
            except NumberParseException as e:
                errores.append(f"{pais}: {e}")

    if not parsed:
        return ValidationResult(False, "syntactic", ["No se pudo interpretar el número"] + errores, None)

    # --- Validaciones ---
    possible = phonenumbers.is_possible_number(parsed)
    valid = phonenumbers.is_valid_number(parsed)

    try:
        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except Exception:
        e164 = None

    region = None
    try:
        region = region_code_for_number(parsed)
    except Exception:
        pass

    num_type = None
    try:
        num_type = _number_type_name(phonenumbers.number_type(parsed))
    except Exception:
        pass

    meta = PhoneValidationMeta(
        e164=e164,
        region=region,
        country_code=getattr(parsed, "country_code", None),
        number_type=num_type,
        possible=possible,
        valid=valid,
        raw_input=raw_in,
    )

    # --- Reglas de decisión ---
    if not possible:
        return ValidationResult(False, "syntactic", ["Número con longitud o formato no válido"], e164)

    if region not in PAISES_ADMITIDOS:
        return ValidationResult(False, "semantic", [f"Número no pertenece a los países admitidos: {PAISES_ADMITIDOS}"], e164)

    if not valid:
        # Aceptamos el formato, aunque no esté asignado
        return ValidationResult(True, "syntactic", ["Formato correcto (número no verificado en red real)"], e164)

    # --- Éxito ---
    messages = [
        "Número telefónico válido",
        f"Región detectada: {meta.region}",
        f"Tipo: {meta.number_type or 'Desconocido'}",
        f"Código país: +{meta.country_code}" if meta.country_code else "",
    ]
    messages = [m for m in messages if m]

    return ValidationResult(True, "semantic", messages, e164)


def normalize_phone(raw: str, country_hint: Optional[str] = None) -> Optional[str]:
    """Devuelve la forma E.164 o None si no es posible."""
    res = validate_phone(raw, country_hint=country_hint)
    return res.normalized if res.success else None

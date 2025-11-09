# src/validators/password_validator.py
from typing import Optional, Dict, Any
from zxcvbn import zxcvbn
from ._types import ValidationResult
from .common import RE_UPPER, RE_LOWER, RE_DIGIT, RE_SPECIAL, RE_WHITESPACE

# Política por defecto (configurable más tarde)
MIN_LENGTH = 12
MIN_UPPER = 1
MIN_LOWER = 1
MIN_DIGITS = 1
MIN_SPECIAL = 2
MIN_ZXC_SCORE = 3  # 0..4, queremos al menos 3 (buena)
COMMON_PASSWORDS = {
    "123456", "123456789", "qwerty", "password", "111111", "12345678",
    "abc123", "1234567", "password1", "12345"
}

def _count_regex(pattern, s: str) -> int:
    return len(pattern.findall(s))

def validate_password(password: str, context: Optional[Dict[str, str]] = None) -> ValidationResult:
    """
    Valida fortaleza de contraseña.
    context: dict opcional con claves como 'username' o 'email_local' para evitar inclusión.
    Devuelve ValidationResult con mensajes accionables.
    """
    pwd = (password or "")
    if not pwd:
        return ValidationResult(False, "lexical", ["Contraseña vacía"], None)

    if RE_WHITESPACE.search(pwd):
        return ValidationResult(False, "syntactic", ["La contraseña no puede contener espacios en blanco"], None)

    messages = []

    if len(pwd) < MIN_LENGTH:
        messages.append(f"Longitud mínima requerida: {MIN_LENGTH} caracteres (actual: {len(pwd)})")

    if _count_regex(RE_UPPER, pwd) < MIN_UPPER:
        messages.append(f"Se requiere al menos {MIN_UPPER} letra(s) mayúscula(s).")

    if _count_regex(RE_LOWER, pwd) < MIN_LOWER:
        messages.append(f"Se requiere al menos {MIN_LOWER} letra(s) minúscula(s).")

    if _count_regex(RE_DIGIT, pwd) < MIN_DIGITS:
        messages.append(f"Se requiere al menos {MIN_DIGITS} dígito(s).")

    if _count_regex(RE_SPECIAL, pwd) < MIN_SPECIAL:
        messages.append(f"Se requieren al menos {MIN_SPECIAL} caracteres especiales (ej. {', '.join(list('!@#$%'))}).")

    # blacklist simple
    if pwd.lower() in COMMON_PASSWORDS:
        messages.append("Contraseña común o débil (lista negra).")

    # context checks: evitar incuir username/email localpart
    if context:
        user = context.get("username")
        email_local = context.get("email_local")
        if user and user.lower() in pwd.lower():
            messages.append("La contraseña no debe contener el nombre de usuario.")
        if email_local and email_local.lower() in pwd.lower():
            messages.append("La contraseña no debe contener la parte local del correo.")

    # zxcvbn analysis
    try:
        z = zxcvbn(pwd, user_inputs=[v for v in (context or {}).values()])
        score = z.get("score", 0)
        feedback = z.get("feedback", {}) or {}
        # ofrecer sugerencias si existen
        suggestions = []
        if feedback.get("suggestions"):
            suggestions.extend(feedback["suggestions"])
        if feedback.get("warning"):
            suggestions.append(feedback["warning"])
    except Exception:
        # en caso de fallo de zxcvbn, lo ignoramos pero dejamos que las reglas básicas actúen
        score = 0
        suggestions = ["No fue posible completar análisis de entropía (zxcvbn fallo)"]

    # si tenemos errores previos, devolvemos fallo sintáctico/semántico según el caso
    if messages:
        # combinar mensajes con sugerencias de zxcvbn
        messages.extend(suggestions)
        return ValidationResult(False, "syntactic", messages, None)

    # ahora validar score
    if score < MIN_ZXC_SCORE:
        m = [f"Análisis de fuerza insuficiente (score zxcvbn={score}/4)."]
        m.extend(suggestions)
        return ValidationResult(False, "semantic", m, None)

    # OK
    success_msgs = [f"Contraseña cumple reglas básicas y obtuvo score zxcvbn={score}/4"]
    if suggestions:
        success_msgs.extend(suggestions)
    # Normalizamos: no cambia la contraseña, así que devolvemos None para normalized por seguridad
    return ValidationResult(True, "semantic", success_msgs, None)

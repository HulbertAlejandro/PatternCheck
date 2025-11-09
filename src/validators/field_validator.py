"""
field_validator.py
------------------
Módulo principal de validación multinivel.
Orquesta la ejecución de validadores individuales según el tipo de campo,
integrando los resultados léxicos, sintácticos y semánticos.

Autor: Hulbert Arango & Asistente GPT-5
Proyecto: Sistema de Validación de Patrones con Regex y AFD
"""

from typing import Dict, Any, Optional
from .validators_registry import get_validator
from ._types import ValidationResult


class FieldValidator:
    """
    Clase principal que centraliza la validación de cualquier campo de entrada.

    Métodos principales:
    - validate_field: ejecuta la validación completa según tipo de campo
    - register_custom_validator: permite añadir validadores personalizados
    """

    def __init__(self):
        # Diccionario de validadores registrados dinámicamente
        self.custom_validators: Dict[str, Any] = {}

    def register_custom_validator(self, name: str, func) -> None:
        """
        Permite registrar validadores personalizados a nivel de ejecución.
        Ejemplo:
            validator.register_custom_validator("ruc", validate_ruc_ecuador)
        """
        if not callable(func):
            raise TypeError(f"El validador '{name}' no es una función válida.")
        self.custom_validators[name.lower()] = func

    def _resolve_validator(self, field_type: str):
        """
        Busca el validador adecuado según el tipo de campo.
        Prioriza validadores personalizados; si no existe, usa los estándar.
        """
        field_type = field_type.lower()
        if field_type in self.custom_validators:
            return self.custom_validators[field_type]
        try:
            return get_validator(field_type)
        except KeyError:
            raise ValueError(f"No existe validador definido para el campo '{field_type}'")

    def validate_field(
        self,
        field_type: str,
        value: Any,
        **kwargs
    ) -> ValidationResult:
        """
        Ejecuta la validación completa de un campo.
        Parámetros:
            - field_type: tipo de dato ('email', 'password', 'phone', etc.)
            - value: valor a validar
            - kwargs: parámetros adicionales específicos del validador (ej. country='MX')

        Retorna:
            ValidationResult: con estado (True/False), nivel y mensajes
        """
        try:
            validator_fn = self._resolve_validator(field_type)
        except Exception as e:
            return ValidationResult(False, "lexical", [str(e)], None)

        try:
            result = validator_fn(value, **kwargs)
            if not isinstance(result, ValidationResult):
                raise TypeError(f"El validador '{field_type}' no devolvió un ValidationResult.")
            return result
        except Exception as e:
            return ValidationResult(False, "semantic", [f"Error en validador '{field_type}': {e}"], None)

    def bulk_validate(self, data: Dict[str, Any], schema: Dict[str, str]) -> Dict[str, ValidationResult]:
        """
        Valida múltiples campos de acuerdo a un esquema:
            schema = {
                "correo": "email",
                "clave": "password",
                "telefono": "phone"
            }
        Retorna un diccionario con los resultados por campo.
        """
        results: Dict[str, ValidationResult] = {}

        for field, field_type in schema.items():
            value = data.get(field, "")
            results[field] = self.validate_field(field_type, value)

        return results


# Instancia global (singleton ligero)
field_validator = FieldValidator()


# --- Ejemplo de uso directo ---
if __name__ == "__main__":
    sample_data = {
        "correo": "usuario@test.com",
        "clave": "Abcd1234@",
        "telefono": "+573004567890",
        "fecha": "29/02/2024",
    }

    schema = {
        "correo": "email",
        "clave": "password",
        "telefono": "phone",
        "fecha": "date",
    }

    results = field_validator.bulk_validate(sample_data, schema)
    for campo, resultado in results.items():
        print(f"{campo}: {resultado}")

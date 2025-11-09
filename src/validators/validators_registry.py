# src/validators/validators_registry.py
from typing import Dict, Callable
from .email_validator import validate_email
from .phone_validator import validate_phone
from .password_validator import validate_password
from .date_validator import validate_date
from .id_validator import validate_id
from .postal_validator import validate_postal
from .plate_validator import validate_plate
from .url_validator import validate_url
from .pattern_validator import validate_pattern

VALIDATOR_REGISTRY: Dict[str, Callable] = {
    "email": validate_email,
    "phone": validate_phone,
    "password": validate_password,
    "date": validate_date,
    "id": validate_id,
    "postal": validate_postal,
    "plate": validate_plate,
    "url": validate_url,
    "pattern": validate_pattern,
}

def get_validator(name: str) -> Callable:
    """Devuelve la función de validación asociada a un campo."""
    fn = VALIDATOR_REGISTRY.get(name.lower())
    if not fn:
        raise KeyError(f"No existe validador registrado para '{name}'")
    return fn

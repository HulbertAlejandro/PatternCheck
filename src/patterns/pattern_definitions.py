# src/patterns/pattern_definitions.py
from typing import Dict, List
from src.validators.pattern_validator import PatternSpec

# Definiciones de patrones como objetos PatternSpec
PATTERNS: Dict[str, PatternSpec] = {
    "email": PatternSpec(
        name="email",
        regex=r"(?i)\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b",
        description="Correo electrónico con formato usuario@dominio.ext",
        examples={
            "valid": ["user@example.com", "test.name+tag@sub-domain.co"],
            "invalid": ["user@", "@domain.com", "user@domain"]
        },
    ),
    "url": PatternSpec(
        name="url",
        regex=r"\bhttps?://[\w\-._~:/?#[\]@!$&'()*+,;=%]+\b",
        description="URLs válidas con protocolo HTTP o HTTPS",
        examples={
            "valid": ["https://www.google.com", "http://example.org/path"],
            "invalid": ["www.google.com", "http//bad-url"]
        },
    ),
    "phone": PatternSpec(
        name="phone",
        regex=r"\b(?:\+?\d{1,3})?[ -]?(?:\(?\d{2,3}\)?)[ -]?\d{3,4}[ -]?\d{4}\b",
        description="Teléfonos internacionales con o sin prefijo país",
        examples={
            "valid": ["+57 320 123 4567", "+1 212 555 0123", "3001234567"],
            "invalid": ["12345", "+57-ABC-123"]
        },
    ),
    "date": PatternSpec(
        name="date",
        regex=r"\b(0[1-9]|[12]\d|3[01])[\/\-](0[1-9]|1[0-2])[\/\-](\d{4})\b",
        description="Fechas válidas en formato DD/MM/YYYY o DD-MM-YYYY",
        examples={
            "valid": ["15/04/2025", "29-02-2024"],
            "invalid": ["31/02/2021", "99/99/9999"]
        },
    ),
    "id": PatternSpec(
        name="id",
        regex=r"\b(?!0{7,10})(?!1234567)\d{7,10}\b",
        description="Cédulas o identificaciones numéricas válidas (7-10 dígitos)",
        examples={
            "valid": ["1032456789", "8765432"],
            "invalid": ["0000000", "1234567"]
        },
    ),
    "password": PatternSpec(
        name="password",
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        description="Contraseña segura (mayúscula, minúscula, número y símbolo)",
        examples={
            "valid": ["Abcd1234!", "Password123@"],
            "invalid": ["abcd1234", "PASSWORD!"]
        },
    ),
    "postal": PatternSpec(
        name="postal",
        regex=r"\b\d{5,6}\b",
        description="Código postal de 5 o 6 dígitos según país",
        examples={
            "valid": ["050001", "110011", "90210"],
            "invalid": ["ABCDE", "1234"]
        },
    ),
    "plate": PatternSpec(
        name="plate",
        regex=r"\b[A-Z]{3}[ -]?\d{3}\b",
        description="Placas vehiculares formato AAA123",
        examples={
            "valid": ["ABC123", "XYZ-789"],
            "invalid": ["12ABC3", "A1B2C3"]
        },
    ),
}

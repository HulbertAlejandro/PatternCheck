# src/validators/common.py
import re
from typing import Pattern

# caracteres especiales considerados para las passwords
SPECIAL_CHARS = r"!@#$%^&*()-_=+[]{}|;:',.<>/?`~\"\\"

# regexes útiles
RE_UPPER = re.compile(r"[A-Z]")
RE_LOWER = re.compile(r"[a-z]")
RE_DIGIT = re.compile(r"\d")
RE_SPECIAL = re.compile(rf"[{re.escape(SPECIAL_CHARS)}]")
RE_WHITESPACE = re.compile(r"\s")
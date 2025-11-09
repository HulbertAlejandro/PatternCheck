# src/validators/pattern_validator.py
import re
from typing import Callable, Optional, Dict, List
from ._types import ValidationResult

class PatternSpec:
    def __init__(self, name: str, regex: str, description: str,
                 examples: Dict[str, List[str]], post_check: Optional[Callable[[str], bool]] = None):
        self.name = name
        self.regex = re.compile(regex)
        self.description = description
        self.examples = examples
        self.post_check = post_check

def validate_pattern(spec: PatternSpec, value: str) -> ValidationResult:
    if not value or not value.strip():
        return ValidationResult(False, "lexical", [f"Valor vacío para patrón {spec.name}"], None)

    s = value.strip()
    if not spec.regex.match(s):
        return ValidationResult(False, "syntactic", [f"No coincide con el patrón {spec.name}"], None)

    if spec.post_check and not spec.post_check(s):
        return ValidationResult(False, "semantic", [f"Falló post-check semántico para {spec.name}"], None)

    return ValidationResult(True, "semantic", [f"Valor válido para patrón {spec.name}"], s)

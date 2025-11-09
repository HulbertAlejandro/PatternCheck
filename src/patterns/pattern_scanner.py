# src/patterns/pattern_scanner.py
import re
from typing import Dict, List, Any
from src.validators._types import ValidationResult
from .pattern_definitions import PATTERNS

class PatternScanner:
    """
    Escáner léxico que detecta patrones conocidos dentro de un texto.
    Utiliza las expresiones regulares definidas en pattern_definitions.py
    """

    def __init__(self, patterns: Dict[str, Any] = PATTERNS):
        self.patterns = patterns

    def scan_text(self, text: str) -> Dict[str, List[str]]:
        """Busca coincidencias de todos los patrones en el texto."""
        results: Dict[str, List[str]] = {}
        for name, spec in self.patterns.items():
            matches = re.findall(spec.regex, text)
            if matches:
                # matches puede ser una lista de tuplas si hay grupos
                flat = ["".join(m) if isinstance(m, tuple) else m for m in matches]
                results[name] = list(set(flat))
        return results

    def validate_token(self, token: str, pattern_name: str) -> ValidationResult:
        """Valida un token individual contra un patrón específico."""
        if pattern_name not in self.patterns:
            return ValidationResult(False, "lexical", [f"Patrón {pattern_name} no definido"], token)

        spec = self.patterns[pattern_name]
        if re.fullmatch(spec.regex, token):
            return ValidationResult(True, "semantic", [f"Token válido para {pattern_name}"], token)
        return ValidationResult(False, "syntactic", [f"No coincide con el patrón {pattern_name}"], token)

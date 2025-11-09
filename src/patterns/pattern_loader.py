# src/patterns/pattern_loader.py
import json
from pathlib import Path
from typing import Dict
from src.validators.pattern_validator import PatternSpec

class PatternLoader:
    """
    Carga patrones definidos externamente (JSON o YAML)
    para ampliar el sistema sin modificar el código fuente.
    """

    @staticmethod
    def load_from_json(path: str) -> Dict[str, PatternSpec]:
        file = Path(path)
        if not file.exists():
            raise FileNotFoundError(f"No se encontró el archivo de patrones: {path}")

        data = json.loads(file.read_text(encoding="utf-8"))
        patterns: Dict[str, PatternSpec] = {}

        for name, info in data.items():
            patterns[name] = PatternSpec(
                name=name,
                regex=info["regex"],
                description=info.get("description", ""),
                examples=info.get("examples", {}),
            )
        return patterns

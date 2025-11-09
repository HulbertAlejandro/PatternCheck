# src/validators/_types.py
from dataclasses import dataclass
from typing import List, Optional, Literal

Level = Literal["lexical", "syntactic", "semantic"]

@dataclass
class ValidationResult:
    success: bool
    level: Level
    messages: List[str]
    normalized: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "level": self.level,
            "messages": self.messages,
            "normalized": self.normalized,
        }
# src/patterns/afd.py
from typing import Dict, Set, Optional, Tuple

class DeterministicFiniteAutomaton:
    """
    Implementación simplificada de un Autómata Finito Determinista (AFD).
    Utilizado para representar gráficamente o validar expresiones regulares
    dentro del marco teórico de lenguajes formales.
    """

    def __init__(self, states: Set[str], alphabet: Set[str],
                 transitions: Dict[Tuple[str, str], str],
                 start_state: str, accept_states: Set[str]):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def process(self, input_string: str) -> bool:
        """Procesa una cadena y determina si es aceptada por el AFD."""
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            transition_key = (current_state, symbol)
            if transition_key not in self.transitions:
                return False
            current_state = self.transitions[transition_key]
        return current_state in self.accept_states

    def describe(self) -> str:
        """Devuelve una representación textual del AFD."""
        desc = ["--- AFD ---"]
        desc.append(f"Estados: {self.states}")
        desc.append(f"Alfabeto: {self.alphabet}")
        desc.append(f"Inicio: {self.start_state}")
        desc.append(f"Aceptación: {self.accept_states}")
        desc.append(f"Transiciones:")
        for (s, sym), dest in self.transitions.items():
            desc.append(f"  δ({s}, '{sym}') → {dest}")
        return "\n".join(desc)

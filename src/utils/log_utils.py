"""
log_utils.py
-------------
Sistema básico de registro de validaciones, advertencias y errores.
Guarda logs en memoria y opcionalmente permite exportarlos.

"""

from datetime import datetime
from typing import List, Dict, Literal

LogLevel = Literal["INFO", "WARNING", "ERROR"]

# Estructura en memoria para logs de sesión
_LOG_HISTORY: List[Dict[str, str]] = []


def log_event(level: LogLevel, message: str, source: str = "system") -> None:
    """
    Registra un evento en la bitácora del sistema.

    Parámetros:
        level (str): Nivel del log ('INFO', 'WARNING', 'ERROR')
        message (str): Descripción del evento
        source (str): Módulo origen del evento
    """
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": level.upper(),
        "source": source,
        "message": message,
    }
    _LOG_HISTORY.append(entry)
    print(f"[{entry['timestamp']}] [{entry['level']}] {entry['source']}: {entry['message']}")


def get_log_history(level: LogLevel | None = None) -> List[Dict[str, str]]:
    """
    Devuelve los registros almacenados en memoria.

    Parámetros:
        level (str | None): Si se especifica, filtra por nivel.

    Retorna:
        list[dict]: Lista de registros de log.
    """
    if level:
        return [log for log in _LOG_HISTORY if log["level"] == level.upper()]
    return list(_LOG_HISTORY)

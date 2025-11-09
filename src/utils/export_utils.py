"""
export_utils.py
----------------
Funciones para exportar resultados de análisis o validaciones
a formatos estándar: CSV y JSON.

Requiere:
    pip install pandas
"""

import pandas as pd
import json
from typing import List, Dict, Any, Optional

def export_to_csv(data: List[Dict[str, Any]], path: str) -> bool:
    """
    Exporta una lista de diccionarios a un archivo CSV.

    Parámetros:
        data (list[dict]): Datos a exportar.
        path (str): Ruta de salida del archivo CSV.

    Retorna:
        bool: True si la exportación fue exitosa.
    """
    try:
        df = pd.DataFrame(data)
        df.to_csv(path, index=False, encoding="utf-8-sig")
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo exportar a CSV: {e}")
        return False


def export_to_json(data: Any, path: str, indent: int = 4) -> bool:
    """
    Exporta datos a formato JSON legible.

    Parámetros:
        data (Any): Estructura de datos (lista, dict, etc.).
        path (str): Ruta del archivo de salida.
        indent (int): Niveles de indentación (por defecto 4).

    Retorna:
        bool: True si se exportó correctamente.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo exportar a JSON: {e}")
        return False

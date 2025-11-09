# src/core/report_generator.py
"""
report_generator.py
-------------------
Genera reportes de resultados de validación o escaneo.
Permite exportar los datos a CSV, JSON o generar un resumen textual.
"""

from typing import List, Dict, Any
from src.utils.export_utils import export_to_csv, export_to_json
from src.utils.log_utils import log_event


def generate_summary(data: List[Dict[str, Any]]) -> str:
    """
    Genera un resumen de resultados en formato texto.
    """
    total = len(data)
    resumen = [f"Total de patrones detectados: {total}"]
    tipos = {}

    for item in data:
        tipo = item.get("tipo") or item.get("pattern", "Desconocido")
        tipos[tipo] = tipos.get(tipo, 0) + 1

    for tipo, count in tipos.items():
        resumen.append(f" - {tipo}: {count} coincidencias")

    summary_text = "\n".join(resumen)
    log_event("INFO", "Resumen generado correctamente", "report_generator")
    return summary_text


def generate_report(data: List[Dict[str, Any]], path: str, format: str = "json") -> bool:
    """
    Exporta un reporte a CSV o JSON según formato especificado.
    """
    try:
        if format.lower() == "csv":
            result = export_to_csv(data, path)
        elif format.lower() == "json":
            result = export_to_json(data, path)
        else:
            log_event("ERROR", f"Formato de exportación no soportado: {format}", "report_generator")
            return False

        if result:
            log_event("INFO", f"Reporte exportado correctamente: {path}", "report_generator")
        return result
    except Exception as e:
        log_event("ERROR", f"Error generando reporte: {e}", "report_generator")
        return False

"""
file_utils.py
-------------
Funciones auxiliares para la lectura y extracción de texto desde archivos.
Admite formatos de texto plano (.txt) y PDF (.pdf).

Requiere:
    pip install PyMuPDF
"""

import fitz  # PyMuPDF
from typing import Optional

def read_text_file(path: str, encoding: str = "utf-8") -> Optional[str]:
    """
    Lee un archivo de texto plano y devuelve su contenido como cadena.

    Parámetros:
        path (str): Ruta del archivo .txt
        encoding (str): Codificación a usar (por defecto 'utf-8')

    Retorna:
        str | None: Contenido del archivo o None si ocurre un error
    """
    try:
        with open(path, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"[ERROR] No se pudo leer el archivo {path}: {e}")
        return None


def extract_text_from_pdf(path: str) -> Optional[str]:
    """
    Extrae texto de un archivo PDF completo.

    Parámetros:
        path (str): Ruta al archivo PDF.

    Retorna:
        str | None: Texto extraído o None si ocurre un error.
    """
    try:
        doc = fitz.open(path)
        text = ""
        for page in doc:
            page_text = page.get_text("text")
            text += str(page_text) + "\n"
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"[ERROR] No se pudo extraer texto del PDF {path}: {e}")
        return None

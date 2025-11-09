"""
Módulo utilitario general.
Contiene funciones de apoyo reutilizables para validación, análisis y exportación.

"""
from .file_utils import read_text_file, extract_text_from_pdf
from .export_utils import export_to_csv, export_to_json
from .log_utils import log_event, get_log_history

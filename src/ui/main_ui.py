# src/ui/main_ui.py
import streamlit as st
from src.ui.components.sidebar import show_sidebar
from src.ui.components.validator_form import show_validator_form
from src.ui.components.scanner_panel import show_scanner_panel
from src.ui.components.layout_utils import apply_custom_styles
from src.ui.components.documentation_mode import show_documentation_mode


def main():
    st.set_page_config(
        page_title="Sistema de Validación de Patrones",
        page_icon=None,
        layout="wide"
    )

    # Aplicar estilos generales
    apply_custom_styles()

    # Obtener la página seleccionada desde la barra lateral
    selected_page = show_sidebar()

    # Espaciado visual superior
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Renderizado de cada modo de la aplicación
    if selected_page == "Validación de Campos":
        show_validator_form()
    elif selected_page == "Escáner de Texto":
        show_scanner_panel()
    elif selected_page == "Documentación Técnica":
        show_documentation_mode()
    else:
        st.info("Seleccione una opción en el menú lateral para comenzar.")


if __name__ == "__main__":
    main()

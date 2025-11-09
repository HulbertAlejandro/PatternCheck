"""
Punto de entrada principal del Sistema de Validación de Patrones
---------------------------------------------------------------
Ejecuta la aplicación Streamlit con la interfaz principal.
"""

import streamlit as st
from src.ui.main_ui import main

if __name__ == "__main__":
    st.set_page_config(
        page_title="Sistema de Validación de Patrones",
        layout="wide"
    )
    main()

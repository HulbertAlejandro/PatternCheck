# src/ui/components/sidebar.py
import streamlit as st

def show_sidebar() -> str:
    """
    Muestra una barra lateral moderna y sobria para la navegación principal.
    Retorna el nombre de la página seleccionada.
    """

    # Estilos personalizados
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            background-color: #162A47;
            padding: 22px 18px;
        }
        .sidebar-title {
            color: #FFFFFF;
            font-size: 21px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
            margin-bottom: 12px;
        }
        .sidebar-subtitle {
            color: #AAB6BF;
            font-size: 13px;
            margin-bottom: 28px;
            font-family: 'Segoe UI', sans-serif;
        }
        div[data-testid="stRadio"] label {
            color: #E0E0E0 !important;
            font-size: 15px !important;
            padding: 8px 12px !important;
            font-family: 'Segoe UI', sans-serif;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label[data-baseweb="radio"]:has(input:checked) {
            background-color: rgba(255, 255, 255, 0.08);
            border-radius: 6px;
        }
        hr {
            border: 0;
            height: 1px;
            background-color: rgba(255, 255, 255, 0.15);
            margin: 20px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Contenido de la barra lateral
    with st.sidebar:
        st.markdown("<div class='sidebar-title'>Sistema de Validación</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-subtitle'>Proyecto de Lenguajes Formales</div>", unsafe_allow_html=True)

        # Navegación principal (agregamos la opción nueva)
        opciones = ["Validación de Campos", "Escáner de Texto", "Documentación Técnica"]

        page = st.radio(
            "Navegación",
            opciones,
            label_visibility="collapsed",
            index=0 if "current_page" not in st.session_state else
            opciones.index(st.session_state["current_page"])
        )

        st.session_state["current_page"] = page

        st.markdown("<hr>", unsafe_allow_html=True)

    return page

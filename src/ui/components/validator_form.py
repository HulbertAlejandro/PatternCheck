# src/ui/components/validator_form.py
import streamlit as st
from src.validators.field_validator import field_validator


def show_validator_form():
    """
    Interfaz principal del modo de Validación de Campos.
    Permite ingresar distintos tipos de valores (email, contraseña, teléfono, fecha, ID, postal, placa, URL)
    y validarlos aplicando análisis léxico, sintáctico y semántico.
    """

    # --- Ajuste visual general ---
    st.markdown(
        """
        <style>
        div.block-container { padding-top: 1rem !important; }
        div[data-testid="stForm"] {
            background-color: transparent !important;
            box-shadow: none !important;
            border: none !important;
            padding: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Encabezado principal ---
    st.markdown(
        """
        <div style="margin-bottom: 10px;">
            <h2 style="color:#E3F2FD; margin-bottom:0;">Validación de Campos</h2>
            <p style="color:#B0BEC5; font-size:15px; margin-top:4px;">
                Ingrese uno o más valores para validar su formato y consistencia según su tipo.
                Cada campo aplica reglas de análisis léxico, sintáctico y semántico basadas en expresiones regulares
                y validadores específicos definidos en el sistema.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Formulario de entrada ---
    with st.form("validation_form", clear_on_submit=False):
        st.markdown("### Datos de Validación", unsafe_allow_html=True)

        st.text("Complete los campos que desee validar:")

        email = st.text_input("Correo Electrónico", placeholder="usuario@dominio.com")
        password = st.text_input("Contraseña", type="password", placeholder="Abcd1234@")
        phone = st.text_input("Teléfono", placeholder="+57 300 123 4567")
        date = st.text_input("Fecha", placeholder="dd/mm/yyyy o dd-mm-yyyy")
        id_num = st.text_input("Cédula / ID", placeholder="1032456789")
        postal = st.text_input("Código Postal", placeholder="050001")
        plate = st.text_input("Placa Vehicular", placeholder="ABC123 o XYZ-789")
        url = st.text_input("URL", placeholder="https://sitio.com")

        submitted = st.form_submit_button("Validar")

    # --- Procesamiento de resultados ---
    if submitted:
        # Mapa del esquema → validador correspondiente
        schema = {
            "email": "email",
            "password": "password",
            "phone": "phone",
            "date": "date",
            "id_num": "id",
            "postal": "postal",
            "plate": "plate",
            "url": "url",
        }

        # Valores ingresados
        data = {
            "email": email.strip(),
            "password": password.strip(),
            "phone": phone.strip(),
            "date": date.strip(),
            "id_num": id_num.strip(),
            "postal": postal.strip(),
            "plate": plate.strip(),
            "url": url.strip(),
        }

        # Filtrar solo los campos llenos
        filled_data = {k: v for k, v in data.items() if v}

        if not filled_data:
            st.info("No se ingresó ningún campo para validar.")
            return

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Resultados de Validación", unsafe_allow_html=True)

        # Ejecutar las validaciones en bloque
        results = field_validator.bulk_validate(filled_data, schema)

        # Mostrar resultados de cada campo
        for field, result in results.items():
            if result.success:
                color = "#1565C0"
                background = "rgba(21, 101, 192, 0.25)"
                message = result.messages[0] if result.messages else "Campo válido"
            else:
                color = "#C62828"
                background = "rgba(198, 40, 40, 0.25)"
                message = result.messages[0] if result.messages else "Campo inválido"

            st.markdown(
                f"""
                <div style="
                    padding:12px;
                    border-left:5px solid {color};
                    background-color:{background};
                    margin-bottom:10px;
                    border-radius:6px;
                ">
                    <strong style="color:#ECEFF1;">{field.title()}</strong><br>
                    <span style="color:#E0E0E0;">{message}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # --- Información complementaria ---
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Descripción de las Validaciones", unsafe_allow_html=True)

        st.markdown("""
        - **Correo Electrónico:** Se valida el formato según RFC, dominios válidos y TLD correctos.
        - **Contraseña:** Se analiza la entropía y complejidad (mayúsculas, minúsculas, números, símbolos, longitud mínima).
        - **Teléfono:** Se valida el formato E.164 con `phonenumbers`, verificando país y tipo de número.
        - **Fecha:** Se verifica formato y validez real (rango 1900–2100, control de bisiestos).
        - **Cédula / ID:** Valida longitud, formato y evita secuencias triviales.
        - **Código Postal:** Comprueba formato según país (Colombia, México, EE.UU., España, Argentina).
        - **Placa Vehicular:** Verifica patrones regionales (CO, MX, US, AR) con letras y números en el formato correcto.
        - **URL:** Se asegura la presencia de protocolo, dominio válido y opcionalmente HTTPS.
        """)

        st.success("Validaciones completadas correctamente.")

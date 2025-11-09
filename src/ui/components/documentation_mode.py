"""
Módulo de Interfaz - Documentación Técnica Ampliada
===================================================

Interfaz Streamlit para el modo de documentación técnica y teórica.
Integra el marco conceptual, la explicación técnica de los validadores,
y la descripción de los patrones definidos en el sistema.

Autores: Hulbert Arango & Asistente GPT-5
Proyecto: Sistema de Búsqueda y Validación de Patrones en Textos y Formularios Interactivos
"""

import streamlit as st
import pandas as pd
from src.validators.field_validator import field_validator
from src.patterns.pattern_definitions import PATTERNS


def show_documentation_mode():
    st.title("Documentación Técnica del Sistema de Validación de Patrones")
    st.markdown("---")

    # -----------------------------------------------------------
    # 1. Descripción General del Proyecto
    # -----------------------------------------------------------
    st.header("1. Descripción General del Proyecto")
    st.write("""
    El proyecto implementa un **sistema integral para la detección y validación de patrones**
    en textos y formularios, aplicando los principios de los **lenguajes formales**, la **teoría de autómatas**
    y el **análisis léxico y sintáctico** mediante expresiones regulares (regex).

    Los patrones definidos se utilizan tanto para **análisis léxico en textos** como para **validación de datos en formularios**,
    garantizando que la información cumpla estructuras coherentes y reglas semánticas específicas.
    """)

    # -----------------------------------------------------------
    # 2. Resultados de Aprendizaje
    # -----------------------------------------------------------
    st.header("2. Resultados de Aprendizaje (RA)")
    st.write("""
    - **RA1:** Aplicar el análisis léxico y sintáctico mediante expresiones regulares para validar estructuras de texto.  
    - **RA2:** Relacionar los autómatas finitos deterministas con las expresiones regulares.  
    - **RA3:** Implementar los conceptos de lenguajes formales en una herramienta práctica de software.
    """)

    # -----------------------------------------------------------
    # 3. Marco Teórico y Conceptual
    # -----------------------------------------------------------
    st.header("3. Marco Teórico y Conceptual")

    st.subheader("3.1 Lenguajes Formales y Expresiones Regulares")
    st.write("""
    En teoría de lenguajes formales, un **lenguaje regular** es aquel que puede ser reconocido por un
    **Autómata Finito Determinista (AFD)** o generado por una **Gramática Regular (Tipo 3)**.
    Las **expresiones regulares (regex)** son una representación algebraica de dichos lenguajes.
    """)

    st.subheader("3.2 Análisis Léxico, Sintáctico y Semántico")
    st.write("""
    Cada validación en este sistema pasa por tres niveles:
    - **Nivel Léxico:** Detecta caracteres o símbolos inválidos.
    - **Nivel Sintáctico:** Comprueba que la estructura se ajuste al patrón (regex o AFD).
    - **Nivel Semántico:** Evalúa el significado del dato (por ejemplo, fechas reales o dominios válidos).
    """)

    st.subheader("3.3 Autómatas Finitos Deterministas (AFD)")
    st.write("""
    Los AFD implementados en el módulo `afd.py` representan el funcionamiento interno de un patrón.
    Cada expresión regular puede transformarse en un conjunto de **estados (Q)**, un **alfabeto (Σ)**,
    una **función de transición (δ)**, un **estado inicial (q₀)** y un **conjunto de estados de aceptación (F)**.
    """)

    st.subheader("3.4 Gramáticas Regulares Equivalentes")
    st.write("""
    Toda expresión regular puede representarse como una gramática regular.
    Por ejemplo, el patrón de correo electrónico puede verse como:
    ```
    <correo> → <usuario> "@" <dominio> "." <tld>
    <usuario> → <letra> | <letra><usuario>
    <dominio> → <letra> | <letra><dominio>
    <tld> → "com" | "org" | "net" | "co"
    ```
    """)

    # -----------------------------------------------------------
    # 4. Implementación Técnica
    # -----------------------------------------------------------
    st.header("4. Implementación Técnica del Sistema")

    st.write("""
    El proyecto está estructurado modularmente para permitir extensibilidad y mantenimiento:
    - `src/patterns/`: Contiene los patrones base y su definición formal.
    - `src/validators/`: Implementa las funciones de validación léxica, sintáctica y semántica.
    - `src/core/`: Núcleo de generación de reportes y orquestación.
    - `src/utils/`: Funciones auxiliares para exportación y registro.
    - `src/ui/`: Interfaces en Streamlit.
    """)

    st.write("""
    La clase principal `FieldValidator` centraliza la ejecución de todos los validadores,
    devolviendo un objeto `ValidationResult` que resume el estado de la validación y mensajes explicativos.
    """)

    # -----------------------------------------------------------
    # 5. Patrones Definidos en el Sistema
    # -----------------------------------------------------------
    st.header("5. Patrones Definidos y Explicación Teórica")

    for name, pattern in PATTERNS.items():
        with st.expander(f"Patrón: {name.upper()}"):
            st.subheader(f"Expresión Regular de {name}")
            st.code(pattern.regex.pattern, language="regex")

            st.markdown(f"**Descripción:** {pattern.description}")

            st.markdown("**Ejemplos válidos:**")
            st.write(", ".join(pattern.examples.get("valid", [])))

            st.markdown("**Ejemplos inválidos:**")
            st.write(", ".join(pattern.examples.get("invalid", [])))

            # Relación teórica
            st.markdown("**Interpretación Formal:**")
            if name == "email":
                st.write("""
                El patrón de correo electrónico se basa en el reconocimiento de tres componentes:
                1. Parte local (usuario)
                2. Símbolo separador "@"
                3. Dominio con TLD.
                Cada segmento puede representarse como una secuencia de tokens alfanuméricos
                reconocidos por un AFD de tres estados: inicial, usuario, dominio.
                """)
            elif name == "url":
                st.write("""
                Reconoce URLs con los protocolos HTTP o HTTPS.
                Su gramática regular define una secuencia compuesta por:
                - Protocolo → "http" | "https"
                - Símbolo de doble barra "//"
                - Dominio → combinación de letras, dígitos y guiones
                - Rutas opcionales → definidas recursivamente.
                """)
            elif name == "phone":
                st.write("""
                Define un conjunto regular de números telefónicos internacionales.
                El patrón permite opcionalmente el prefijo '+' seguido del código de país,
                agrupaciones de 2-3 dígitos para área, y bloques de 3–4 dígitos de usuario.
                """)
            elif name == "date":
                st.write("""
                Lenguaje regular de fechas válidas en formato DD/MM/YYYY o DD-MM-YYYY.
                El AFD correspondiente recorre posiciones que validan los rangos permitidos
                para días, meses y años de cuatro dígitos.
                """)
            elif name == "id":
                st.write("""
                Reconoce identificaciones numéricas de 7 a 10 dígitos, excluyendo secuencias triviales.
                Se asocia a una gramática regular simple: D → D D | ε, con restricción semántica
                sobre el valor de los dígitos.
                """)
            elif name == "password":
                st.write("""
                Representa un conjunto regular extendido de contraseñas que cumplan con:
                - Presencia de mayúsculas, minúsculas, números y símbolos.
                - Longitud mínima de 8 caracteres.
                Se combina con un análisis semántico posterior para medir la fortaleza.
                """)
            elif name == "postal":
                st.write("""
                Lenguaje de 5 o 6 dígitos según el país.
                Representa un conjunto finito regular definido por la concatenación de símbolos numéricos.
                """)
            elif name == "plate":
                st.write("""
                Reconoce placas vehiculares con formato AAA123 o AAA-123.
                Se modela como un AFD de 7 estados, cada uno correspondiente a una posición fija
                (3 letras, opcional guion, 3 dígitos).
                """)

    # -----------------------------------------------------------
    # 6. Ejecución de Casos de Prueba
    # -----------------------------------------------------------
    st.header("6. Casos de Prueba Representativos")

    casos = {
        "email": "usuario@dominio.com",
        "url": "https://www.python.org",
        "phone": "+573001234567",
        "date": "15/04/2025",
        "id": "1032456789",
        "password": "Abcd1234@",
        "postal": "110011",
        "plate": "ABC123"
    }

    schema = {k: k for k in casos.keys()}
    resultados = field_validator.bulk_validate(casos, schema)

    df = pd.DataFrame([
        {
            "Campo": k,
            "Valor": casos[k],
            "Resultado": "Válido" if r.success else "Inválido",
            "Nivel": r.level,
            "Mensajes": "; ".join(r.messages)
        }
        for k, r in resultados.items()
    ])
    st.dataframe(df, use_container_width=True)

    # -----------------------------------------------------------
    # 7. Fases del Proyecto
    # -----------------------------------------------------------
    st.header("7. Fases del Proyecto")

    st.markdown("""
    **Fase 1. Análisis de requerimientos:**  
    Identificación de ocho patrones principales y definición de reglas formales.

    **Fase 2. Diseño:**  
    Creación de expresiones regulares equivalentes a AFDs.  
    Estructura modular y separación por responsabilidades.

    **Fase 3. Implementación:**  
    Desarrollo de validadores, clase FieldValidator y generación de reportes automáticos.

    **Fase 4. Pruebas:**  
    Validaciones exhaustivas con casos correctos e incorrectos.

    **Fase 5. Documentación:**  
    Elaboración de documentación técnica con teoría de lenguajes formales y autómatas.
    """)

    # -----------------------------------------------------------
    # 8. Conclusión
    # -----------------------------------------------------------
    st.header("8. Conclusión")
    st.write("""
    El sistema demuestra la aplicación práctica de los lenguajes formales
    en el contexto del desarrollo de software.  
    Cada patrón definido corresponde a un lenguaje regular, 
    y su procesamiento mediante expresiones regulares equivale a la ejecución
    de un autómata finito determinista.  
    La integración con Streamlit facilita la validación visual e interactiva,
    permitiendo explorar de forma didáctica los conceptos de análisis léxico y sintáctico.
    """)

    st.markdown("---")
    st.caption("Proyecto: Sistema de Validación de Patrones – 2025")

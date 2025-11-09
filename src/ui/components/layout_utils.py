# src/ui/components/layout_utils.py
import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Encabezados */
        h1, h2, h3, h4 {
            color: #1E3A5F;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Botones */
        .stButton>button {
            background-color: #1E3A5F;
            color: white;
            border-radius: 4px;
            border: none;
            font-weight: 500;
        }

        .stButton>button:hover {
            background-color: #274C77;
        }

        /* Formularios */
        .stForm {
            background-color: #F7F7F7;
            padding: 20px;
            border-radius: 6px;
            border: 1px solid #E0E0E0;
        }

        /* Text Inputs */
        .stTextInput>div>div>input {
            border: 1px solid #D0D0D0;
            border-radius: 6px;
        }
        </style>
    """, unsafe_allow_html=True)

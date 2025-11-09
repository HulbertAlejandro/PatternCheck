# src/ui/components/scanner_panel.py
import streamlit as st
from src.patterns.pattern_scanner import PatternScanner
from src.core.report_generator import generate_summary
import tempfile
import os
from PyPDF2 import PdfReader
import pandas as pd
import json

def _read_uploaded_text_file(uploaded_file):
    try:
        return uploaded_file.read().decode("utf-8", errors="ignore")
    except Exception:
        # fallback binario
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")

def _extract_text_from_pdf_bytes(file_bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    try:
        reader = PdfReader(tmp_path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
    return text

def show_scanner_panel():
    # --- Título ---
    st.markdown(
        """
        <h2 style="color:#E3F2FD; margin-bottom:0;">Escáner de Texto</h2>
        <p style="color:#B0BEC5; font-size:15px; margin-top:4px;">
            Analiza texto o archivos (.txt o .pdf) para detectar patrones: correos, URLs, teléfonos, fechas, etc.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- Entrada ---
    uploaded_file = st.file_uploader("Cargar archivo (.txt o .pdf)", type=["txt", "pdf"])
    text_input = st.text_area(
        "O ingrese el texto directamente:",
        height=200,
        placeholder="Ejemplo: Contacte a soporte@empresa.com o visite https://empresa.com",
    )

    # Botón de análisis
    if st.button("Analizar texto"):
        text = ""

        if uploaded_file:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext == ".txt":
                text = _read_uploaded_text_file(uploaded_file)
            elif ext == ".pdf":
                try:
                    text = _extract_text_from_pdf_bytes(uploaded_file.getvalue())
                except Exception as e:
                    st.error(f"No se pudo procesar el PDF: {e}")
                    return
        else:
            text = text_input or ""

        if not text.strip():
            st.warning("Debe ingresar o cargar un texto antes de analizar.")
            return

        # Ejecutar el escáner (PatternScanner)
        scanner = PatternScanner()
        results = scanner.scan_text(text)

        # Guardar resultados en session_state para persistencia entre reruns
        st.session_state["scan_results"] = results
        # Generar resumen y total
        flat_for_summary = [{"tipo": p, "valor": v} for p, vals in results.items() for v in vals]
        st.session_state["scan_summary_text"] = generate_summary(flat_for_summary)
        st.session_state["scan_total_matches"] = sum(len(vals) for vals in results.values())

    # --- Si ya hay resultados en sesión, los mostramos ---
    results = st.session_state.get("scan_results")
    summary_text = st.session_state.get("scan_summary_text")
    total_matches = st.session_state.get("scan_total_matches")

    if results:
        st.markdown("#### Resultados del Análisis")
        st.markdown("<hr>", unsafe_allow_html=True)
        for pattern, tokens in results.items():
            if not tokens:
                continue
            st.markdown(
                f"""
                <div style="
                    padding:12px;
                    border-left:4px solid #1565C0;
                    background-color:rgba(21, 101, 192, 0.25);
                    margin-bottom:10px;
                    border-radius:6px;
                ">
                    <strong style="color:#ECEFF1;">{pattern.capitalize()}</strong><br>
                    <span style="color:#E0E0E0;">{', '.join(tokens)}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Resumen
        st.markdown("<hr>", unsafe_allow_html=True)
        if summary_text is None:
            # recalcular por seguridad
            flat_for_summary = [{"tipo": p, "valor": v} for p, vals in results.items() for v in vals]
            summary_text = generate_summary(flat_for_summary)
            total_matches = sum(len(vals) for vals in results.values())

        st.markdown(
            f"""
            <div style="
                background-color:rgba(255,255,255,0.05);
                padding:10px;
                border-radius:6px;
                border-left:5px solid #1976D2;
                color:#CFD8DC;
            ">
                <strong>Resumen:</strong><br>
                {summary_text.replace("\\n", "<br>")}
                <br><br>
                Total de coincidencias: <strong>{total_matches}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- Exportar resultados (persistente) ---
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### Exportar Resultados", unsafe_allow_html=True)

        # mantener selección en session_state
        if "export_format" not in st.session_state:
            st.session_state["export_format"] = "JSON"
        export_format = st.radio(
            "Formato de exportación:",
            ["JSON", "CSV"],
            index=0 if st.session_state["export_format"] == "JSON" else 1,
            horizontal=True,
            key="export_format_radio"
        )
        st.session_state["export_format"] = export_format

        # preparar datos para exportar
        export_data = [
            {"Tipo de Patrón": p, "Coincidencia": v}
            for p, vals in results.items() for v in vals
        ]

        # generar bytes en memoria (no archivos temporales)
        if export_format == "JSON":
            payload = json.dumps(export_data, ensure_ascii=False, indent=2).encode("utf-8")
            mime = "application/json"
            fname = "reporte_patrones.json"
        else:  # CSV
            df = pd.DataFrame(export_data)
            payload = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            mime = "text/csv"
            fname = "reporte_patrones.csv"

        st.download_button(
            label=f"Descargar reporte ({export_format})",
            data=payload,
            file_name=fname,
            mime=mime,
        )

    else:
        st.info("No hay resultados para mostrar. Ejecute un análisis primero.")

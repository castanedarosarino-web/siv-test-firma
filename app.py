import streamlit as st
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
from PIL import Image
import io
from datetime import datetime
import numpy as np

st.set_page_config(page_title="S.I.V. - TEST DE FIRMA DIGITAL", layout="centered")

st.title("🖊️ S.I.V. - Módulo de Prueba de Firma")
st.write("Probá firmar en el recuadro y generá el PDF para ver el resultado.")

nombre = st.text_input("Nombre del Firmante", value="SUB COMISARIO CASTAÑEDA JUAN").upper()
dni = st.text_input("DNI", value="27137000")

st.markdown("### FIRME AQUÍ ABAJO")
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 1)",
    stroke_width=3,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=150,
    width=400,
    drawing_mode="freedraw",
    key="canvas",
)

def generar_pdf_con_firma(nombre, dni, imagen_firma):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "ACTA DE PRUEBA DE FIRMA DIGITAL", ln=True, align="C")
    pdf.ln(20)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Por la presente, el llamado {nombre}, con DNI {dni},", ln=True)
    pdf.cell(0, 10, f"valida el contenido del presente documento en fecha {datetime.now().strftime('%d/%m/%Y')}.", ln=True)
    
    pdf.ln(30)
    
    if imagen_firma is not None:
        # CONVERSIÓN CORREGIDA PARA EVITAR EL ERROR 'RFIND'
        img = Image.fromarray(imagen_firma.astype('uint8'), 'RGBA')
        # La convertimos a RGB (fondo blanco) para que FPDF la lea más fácil
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3]) 
        
        img_buffer = io.BytesIO()
        bg.save(img_buffer, format='JPEG')
        img_buffer.seek(0)
        
        # Guardamos temporalmente para que FPDF no busque el nombre del archivo
        pdf.image(bg, x=75, y=pdf.get_y(), w=60)
    
    pdf.ln(25)
    pdf.cell(0, 10, "------------------------------------------", ln=True, align="C")
    pdf.cell(0, 5, "FIRMA DEL INTERESADO", ln=True, align="C")
    
    return pdf.output(dest="S").encode("latin-1", errors="replace")

if st.button("💾 GENERAR PDF DE PRUEBA"):
    if canvas_result.image_data is not None and nombre:
        try:
            pdf_bytes = generar_pdf_con_firma(nombre, dni, canvas_result.image_data)
            st.download_button(
                label="📄 DESCARGAR PDF RESULTANTE",
                data=pdf_bytes,
                file_name=f"test_firma_{dni}.pdf",
                mime="application/pdf"
            )
            st.success("¡PDF generado correctamente!")
        except Exception as e:
            st.error(f"Error al generar PDF: {e}")
    else:
        st.warning("Por favor, ingrese el nombre y firme el recuadro.")

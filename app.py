import streamlit as st
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
from PIL import Image
import io
from datetime import datetime

st.set_page_config(page_title="S.I.V. - TEST DE FIRMA DIGITAL", layout="centered")

st.title("🖊️ S.I.V. - Módulo de Prueba de Firma")
st.write("Probá firmar en el recuadro y generá el PDF para ver el resultado.")

# --- DATOS BÁSICOS ---
nombre = st.text_input("Nombre del Firmante").upper()
dni = st.text_input("DNI")

# --- CONFIGURACIÓN DEL PANEL DE FIRMA ---
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

# --- FUNCIÓN PARA GENERAR PDF CON FIRMA ---
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
    
    # Insertar la firma
    if imagen_firma is not None:
        # Convertir el array del canvas a una imagen de Pillow
        img = Image.fromarray(imagen_firma.astype('uint8'), 'RGBA')
        # Guardarla en un buffer de memoria
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Pegar la imagen en el PDF (posicionada sobre la línea de firma)
        # x, y, ancho (en mm)
        pdf.image(img_buffer, x=75, y=pdf.get_y(), w=60)
    
    pdf.ln(15)
    pdf.cell(0, 10, "------------------------------------------", ln=True, align="C")
    pdf.cell(0, 5, "FIRMA DEL INTERESADO", ln=True, align="C")
    
    return pdf.output(dest="S").encode("latin-1", errors="replace")

# --- BOTÓN DE PROCESAMIENTO ---
if st.button("💾 GENERAR PDF DE PRUEBA"):
    if canvas_result.image_data is not None and nombre:
        pdf_bytes = generar_pdf_con_firma(nombre, dni, canvas_result.image_data)
        st.download_button(
            label="📄 DESCARGAR PDF RESULTANTE",
            data=pdf_bytes,
            file_name=f"test_firma_{dni}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Por favor, ingrese el nombre y firme el recuadro.")

st.markdown("---")
st.info("Nota: Una vez que confirmes que el tamaño de la firma en el PDF es correcto, lo pasamos a tus bloques oficiales.")

import PyPDF2 # Para leer PDF, que esta en bytes. Por ello tenemos que extraer el texto y procesarlo
from io import BytesIO #Es un modulo para leer esos bytes.

def extraer_texto_pdf(archivo_pdf):
    """Extrae el texto del CV del usuario"""
    try:
        archivo_pdf.seek(0)
        pdf_reader = PyPDF2.PdfReader(BytesIO(archivo_pdf.read()))
        texto_completo = ""
        for pagina in pdf_reader.pages:
            texto_completo += pagina.extract_text() + "\n"
        
        return texto_completo.strip()
    except Exception as e:
        return f"Error leyendo PDF: {e}"

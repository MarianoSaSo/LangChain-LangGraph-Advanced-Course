import PyPDF2 # Para leer PDF, que esta en bytes. Por ello tenemos que extraer el texto y procesarlo
from io import BytesIO #Es un modulo para leer esos bytes.

# lee un PDF → extrae el texto → lo devuelve como string
def extraer_texto_pdf(archivo_pdf):
    """Primero lee el texto y despues Extrae el texto del CV del usuario"""
    try:
        archivo_pdf.seek(0)
        pdf_reader = PyPDF2.PdfReader(BytesIO(archivo_pdf.read()))
        texto_completo = ""
        for pagina in pdf_reader.pages:
            texto_completo += pagina.extract_text() + "\n"
        
        return texto_completo.strip()
    except Exception as e:
        return f"Error leyendo PDF: {e}"

#0. archivo_pdf.seek(0) hace que el cursor de lectura del archivo pdf vaya siempre al inicio
#1. archivo_pdf.read() 👉 lee el archivo en bytes
#2. BytesIO(...) 👉 convierte bytes en “archivo virtual”
#3. PdfReader(...) 👉 PyPDF2 abre el PDF y lo interpreta

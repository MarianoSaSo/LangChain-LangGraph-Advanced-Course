import PyPDF2
from io import BytesIO

def extraer_texto_pdf(archivo_pdf):
    """Extrae el contenido de texto de un archivo PDF subido via Streamlit"""
    try:
        # Volvemos al inicio del stream por seguridad
        archivo_pdf.seek(0) 
        pdf_reader = PyPDF2.PdfReader(BytesIO(archivo_pdf.read()))
        texto_completo = ""

        # Recorremos cada página y extraemos el texto
        for numero_pagina, pagina in enumerate(pdf_reader.pages, 1):
            texto_pagina = pagina.extract_text()
            if texto_pagina.strip():
                # No ponemos separadores internos para facilitar el LLM, solo el texto
                texto_completo += f"\n{texto_pagina}\n"
        
        texto_completo = texto_completo.strip()

        if not texto_completo:
            return "Error: El PDF parece estar vacío o contener solo imágenes."
        
        return texto_completo
    
    except Exception as e:
        return f"Error al procesar el archivo PDF: {str(e)}"

import PyPDF2  # Importamos la librería para extraer texto de archivos PDF (instalar con: pip install PyPDF2)
from io import BytesIO  # Módulo para manejar flujos de datos binarios (bytes) en memoria
from utils.logger import logger  # Importamos nuestro sistema de logs para ver lo que ocurre internamente

def extraer_texto_pdf(archivo_pdf):
    """
    Función para extraer el texto de un archivo PDF subido (generalmente como bytes).
    Se encarga de procesar página por página y limpiar el contenido para el LLM.
    """
    
    # Es muy recomendable usar bloques try-except al procesar PDFs, ya que son archivos
    # complejos y pueden ocurrir errores de lectura inesperados.
    try:
        logger.info(f"📂 Iniciando extracción de PDF. Archivo recibido.")
        # Creamos un lector de PDF pasando los bytes del archivo a través de BytesIO
        # Esto permite que PyPDF2 interprete la información binaria correctamente.
        pdf_reader = PyPDF2.PdfReader(BytesIO(archivo_pdf.read()))
        texto_completo = ""

        total_paginas = len(pdf_reader.pages)
        logger.info(f"📑 El PDF tiene {total_paginas} páginas en total.")

        # Iteramos por cada una de las páginas del documento
        # Usamos enumerate(..., 1) para que el número de página empiece en 1 y sea legible
        for numero_pagina, pagina in enumerate(pdf_reader.pages, 1):
            
            # Extraemos el texto crudo de la página actual
            texto_pagina = pagina.extract_text()
            
            # Solo procesamos la página si después de limpiar espacios tiene contenido útil
            if texto_pagina.strip():
                # Añadimos un separador visual para que el LLM sepa dónde empieza cada página
                texto_completo += f"\n--- PÁGINA {numero_pagina} ---\n"
                texto_completo += texto_pagina + "\n"
        
        # Limpieza final: eliminamos espacios en blanco innecesarios al inicio y al final.
        # Esto es vital para no gastar tokens (recursos económicos) con el LLM.
        caracteres_extraidos = len(texto_completo)
        texto_completo = texto_completo.strip()

        # Si tras el proceso no hay texto, informamos que el PDF podría ser solo imágenes
        if not texto_completo:
            logger.warning("⚠️ Extracción fallida: El texto está vacío tras el procesamiento.")
            return "Error: El PDF parece estar vacío o contener solo imágenes."
        
        logger.info(f"✅ Extracción completada: {caracteres_extraidos} caracteres obtenidos.")
        # Retornamos el contenido procesado listo para ser enviado al modelo
        return texto_completo
    
    except Exception as e:
        # Si ocurre cualquier error durante el proceso, lo capturamos y devolvemos el mensaje
        logger.error(f"❌ Error en pdf_processor: {str(e)}")
        return f"Error al procesar el archivo PDF: {str(e)}"

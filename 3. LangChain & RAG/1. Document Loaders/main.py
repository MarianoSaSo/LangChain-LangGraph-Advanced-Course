import os
from dotenv import load_dotenv

# 1. IMPORTACIONES DE LOADERS
# Importamos desde 'langchain_community' las herramientas necesarias.
# - PyPDFLoader: Carga archivos PDF página por página.
# - WebBaseLoader: Carga contenido de una URL (.html estático).
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader

# =================================================================
# TEMA 3: LANGCHAIN & RAG - LECCIÓN 1: DOCUMENT LOADERS
# =================================================================

# OBJETIVO: Aprender a integrar información externa (PDFs, Webs, CSV, etc.) 
# en el ecosistema de LangChain mediante el objeto 'Document'.

# 1. CARGAR CONFIGURACIÓN
load_dotenv()

# --- EJEMPLO 1: CARGAR UN ARCHIVO PDF ---
print("--- PROCESANDO PDF ---")

# Nota: Asegúrate de tener instalado 'pypdf' (pip install pypdf)
try:
    # Ruta al archivo (la calculamos dinámicamente)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(current_dir, "CV Mariano Saez Soriano (E.V.).pdf")

    # Instanciamos el loader con la ruta del PDF
    loader_pdf = PyPDFLoader(pdf_path)

    # .load() devuelve una lista de objetos Document (uno por cada página)
    paginas = loader_pdf.load()

    # Inspeccionamos la primera página para entender la estructura
    if paginas:
        primera_pagina = paginas[0]
        print(f"Páginas totales encontradas: {len(paginas)}")
        print(f"\n--- Contenido de la Página 1 ---\n{primera_pagina.page_content[:500]}...") # Mostramos los primeros 500 caracteres
        print(f"\n--- Metadatos de la Página 1 ---\n{primera_pagina.metadata}")

except Exception as e:
    print(f"⚠️ Error al cargar el PDF: {e}")


print("\n" + "="*50 + "\n")


# --- EJEMPLO 2: CARGAR UNA PÁGINA WEB ---
print("--- PROCESANDO WEB ---")

# Nota: Asegúrate de tener instalado 'beautifulsoup4' (pip install beautifulsoup4)
try:
    # Definimos la URL que queremos analizar
    url = "https://marca.com/" # Usamos el sitio de la lección
    
    # Instanciamos el loader con la URL
    loader_web = WebBaseLoader(url)
    
    # Cargamos el contenido web
    docs_web = loader_web.load()
    
    if docs_web:
        doc_web = docs_web[0]
        print(f"Título detectado: {doc_web.metadata.get('title', 'Sin título')}")
        print(f"\n--- Contenido web (fragmento) ---\n{doc_web.page_content.strip()[:500]}...")

except Exception as e:
    print(f"⚠️ Error al cargar la web: {e}")


# =================================================================
# RESUMEN PARA LOS ESTUDIANTES:
# 1. Todo lo que cargamos con un Loader se convierte en una LISTA de 'Documents'.
# 2. Un 'Document' tiene:
#    - page_content: El texto real que la IA va a procesar.
#    - metadata: El "DNI" del documento (fuente, página, título, etc.).
# 3. La mayoría de los Loaders requieren librerías de apoyo (pypdf, bs4, etc.)
#    porque son integraciones con herramientas externas.
# =================================================================

import os
from dotenv import load_dotenv

# 1. IMPORTACIONES DE LOS LOADERS MÁS INTERESANTES
# Cada una de estas importaciones requiere librerías externas que ya hemos instalado.
from langchain_community.document_loaders import (
    WebBaseLoader,
    YoutubeLoader,
    CSVLoader
)

# =================================================================
# TEMA 3: LANGCHAIN & RAG - LECCIÓN 2: DOCUMENT LOADERS INTERESANTES
# =================================================================

# OBJETIVO: Explorar loaders especializados para extraer información 
# de YouTube, archivos CSV estructurados y webs dinámicas.

# 1. CARGAR CONFIGURACIÓN
load_dotenv()

print("--- INICIANDO EXPLORACIÓN DE LOADERS INTERESANTES ---\n")


# --- EJEMPLO 1: CARGA AVANZADA DE WEB (MÚLTIPLES URLS) ---
print("--- [CASE 1] WEB LOADER (AVANZADO) ---")

urls_interesantes = [
    "https://python.langchain.com/docs/concepts/",
    "https://python.langchain.com/docs/tutorials/"
]

try:
    # El WebBaseLoader puede recibir una lista de URLs de una vez
    loader_web = WebBaseLoader(web_paths=urls_interesantes)
    docs_web = loader_web.load()
    
    print(f"Páginas cargadas: {len(docs_web)}")
    for i, doc in enumerate(docs_web):
        # El metadato 'source' nos dice de qué URL viene cada documento
        print(f"Página {i+1}: {doc.metadata.get('source')} - ({len(doc.page_content)} caracteres)")

except Exception as e:
    print(f"⚠️ Error en WebLoader: {e}")

print("\n" + "-"*50 + "\n")


# --- EJEMPLO 2: YOUTUBE LOADER (EXTRACCIÓN DE TRANSCRIPCIÓN) ---
print("--- [CASE 2] YOUTUBE LOADER ---")

# Nota: Requiere 'youtube-transcript-api' y 'pytube'
# Usamos un ID de video de ejemplo (debes sustituirlo por uno real)
video_url = "https://www.youtube.com/watch?v=AupwoN8QvbU&list=RDeZptwvjKjk4&index=2" # Ejemplo: Video oficial de LangChain (si existiera este ID)

try:
    # add_video_info nos da metadatos como el título o las vistas
    loader_yt = YoutubeLoader.from_youtube_url(
        video_url, 
        add_video_info=True,
        language=["es", "en"]
    )
    
    docs_yt = loader_yt.load()
    
    if docs_yt:
        video_info = docs_yt[0].metadata
        print(f"Película/Video detectado: {video_info.get('title')}")
        print(f"Autor: {video_info.get('author')}")
        print(f"Fragmento de transcripción: {docs_yt[0].page_content[:200]}...")
    
except Exception as e:
    # Es muy común que este falle si el video no tiene subtítulos habilitados
    print(f"⚠️ Nota de YouTube: {e} (Es probable que el video no tenga subtítulos disponibles)")


print("\n" + "-"*50 + "\n")


# --- EJEMPLO 3: CSV LOADER (DATOS ESTRUCTURADOS) ---
print("--- [CASE 3] CSV LOADER ---")

try:
    # Ruta al archivo CSV que acabamos de crear
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "ejemplo_ventas.csv")
    
    # Podemos configurar cómo queremos que se lean las filas
    loader_csv = CSVLoader(
        file_path=csv_path,
        csv_args={
            'delimiter': ',',
            'quotechar': '"'
        }
    )
    
    docs_csv = loader_csv.load()
    
    print(f"Registros encontrados en el CSV: {len(docs_csv)}")
    # Mostramos el primer "Documento" que representa la primera fila del CSV
    if docs_csv:
        print(f"Contenido del primer registro:\n{docs_csv[0].page_content}")
        print(f"Metadatos: {docs_csv[0].metadata}")

except Exception as e:
    print(f"⚠️ Error en CSVLoader: {e}")


# =================================================================
# EXPLICACIÓN PARA LOS ESTUDIANTES:
# 1. Los Loaders avanzados (Google Drive, Youtube, Git) suelen ser integraciones
#    con terceras partes. Requieren atención a permisos y claves.
# 2. El CSVLoader es brutal porque convierte cada fila en un "Document"
#    donde los encabezados de las columnas actúan como etiquetas de contexto.
# 3. El YoutubeLoader por defecto busca subtítulos (transcripciones). 
#    ¡Es una forma increíble de dar "oídos" a nuestra IA!
# =================================================================

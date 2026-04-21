import os
from dotenv import load_dotenv, find_dotenv

# Cargamos las variables de entorno (.env)
load_dotenv(find_dotenv())

# =================================================================
# 📁 CONFIGURACIÓN DE RUTAS (Portabilidad)
# =================================================================

# 1. Obtenemos la ruta absoluta de la carpeta donde reside este archivo 'config.py'.
# - __file__: Es una variable especial de Python que contiene la ruta del archivo actual.
# - os.path.abspath: Convierte cualquier ruta en una ruta absoluta (completa) desde la raíz del sistema.
# - os.path.dirname: Se queda únicamente con la carpeta, eliminando el nombre del archivo 'config.py'.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Construimos las rutas a las carpetas 'docs' y 'chroma_db' de forma dinámica.
# - os.path.join: Es la forma correcta y segura de unir carpetas. Detecta automáticamente
#   si debe usar '\' (Windows) o '/' (Mac/Linux), evitando errores de compatibilidad.
DOCS_PATH = os.path.join(BASE_DIR, "docs")
CHROMADB_PATH = os.path.join(BASE_DIR, "chroma_db")

# Modelos de Inteligencia Artificial - GOOGLE GEMINI
EMBEDDINGS_MODEL = "models/gemini-embedding-001"
CHAT_MODEL = "gemini-1.5-flash"
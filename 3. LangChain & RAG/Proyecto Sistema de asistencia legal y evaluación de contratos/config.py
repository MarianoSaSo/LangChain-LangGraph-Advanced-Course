# =================================================================
# ARCHIVO DE CONFIGURACIÓN - Asistente Legal RAG
# =================================================================
# Aquí centralizamos todos los parámetros configurables del sistema.
# De esta forma, si queremos cambiar un modelo, una ruta o un parámetro,
# no hay que buscar dentro del código: se cambia aquí directamente.

import os

# -----------------------------------------------------------------
# Configuración de modelos (Google Gemini)
# -----------------------------------------------------------------
# Usamos dos modelos distintos para optimizar coste y calidad:
# - QUERY_MODEL: Para tareas de reformulación de consultas (más ligero)
# - GENERATION_MODEL: Para la respuesta final al usuario (más potente)
EMBEDDING_MODEL = "models/gemini-embedding-001"
QUERY_MODEL = "models/gemini-2.5-flash"
GENERATION_MODEL = "models/gemini-2.5-flash"

# -----------------------------------------------------------------
# Configuración del Vector Store (ChromaDB)
# -----------------------------------------------------------------
# Usamos os.path para que la ruta sea relativa al proyecto,
# así funciona en cualquier máquina sin tener que cambiar rutas.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")
CONTRATOS_PATH = os.path.join(BASE_DIR, "contratos")

# Parámetros de división de documentos (Text Splitting)
# Fragmentos más grandes (5000) preservan mejor el contexto de cada cláusula,
# y un overlap alto (1000) asegura que no se pierda información entre cortes.
CHUNK_SIZE = 5000
CHUNK_OVERLAP = 1000

# -----------------------------------------------------------------
# Configuración del Retriever
# -----------------------------------------------------------------
# MMR (Maximal Marginal Relevance) busca documentos relevantes Y diversos,
# evitando que se devuelvan fragmentos casi idénticos.
SEARCH_TYPE = "mmr"
MMR_DIVERSITY_LAMBDA = 0.7   # Balance: 1.0 = solo relevancia, 0.0 = solo diversidad
MMR_FETCH_K = 20             # Documentos iniciales a evaluar antes de aplicar MMR
SEARCH_K = 2                 # Documentos finales que se devolverán al usuario

# Configuración alternativa para retriever híbrido (Ensemble)
ENABLE_HYBRID_SEARCH = True
SIMILARITY_THRESHOLD = 0.70
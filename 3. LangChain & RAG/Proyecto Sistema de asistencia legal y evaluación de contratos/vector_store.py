# =================================================================
# VECTOR STORE - Construcción de la Base de Datos con IA (Enriquecida)
# =================================================================
# Este script es el PRIMER PASO de cualquier aplicación RAG avanzada.
#
# NOVEDAD: No solo dividimos el texto, sino que usamos una IA para
# "leer" cada fragmento antes de guardarlo y extraer entidades clave
# (nombres, fechas, importes). Esto se guarda como METADATOS, lo que
# facilita enormemente que el sistema RAG encuentre la información exacta.
#
# EJECUCIÓN: python vector_store.py
# =================================================================
import langchain
# Parche para evitar errores de atributos faltantes en versiones inconsistentes de LangChain
if not hasattr(langchain, "verbose"):
    langchain.verbose = False
if not hasattr(langchain, "debug"):
    langchain.debug = False
if not hasattr(langchain, "llm_cache"):
    langchain.llm_cache = None

import os
from dotenv import load_dotenv, find_dotenv

# Componentes de LangChain para el pipeline de indexación
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Importamos la configuración y el prompt de extracción
from config import (
    EMBEDDING_MODEL, QUERY_MODEL, CHROMA_DB_PATH, CONTRATOS_PATH,
    CHUNK_SIZE, CHUNK_OVERLAP
)
from prompts import ENTITY_EXTRACTION_PROMPT

# Cargar las credenciales (API Key de Google)
load_dotenv(find_dotenv())


def build_vector_store():
    """
    Construye la base de datos vectorial enriquecida con extracción de entidades.
    """
    print("🌟 Iniciando construcción de la Base de Datos Vectorial Enriquecida...\n")

    # =====================================================================
    # 1. Cargar todos los documentos PDF
    # =====================================================================
    print(f"📂 Cargando documentos PDF desde: {CONTRATOS_PATH}")
    loader = PyPDFDirectoryLoader(CONTRATOS_PATH)
    documentos = loader.load()
    print(f"✅ Se cargaron exitosamente {len(documentos)} páginas.\n")

    # =====================================================================
    # 2. Dividir documentos en fragmentos (chunks)
    # =====================================================================
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    docs_split = text_splitter.split_documents(documentos)
    print(f"✂️ Se crearon {len(docs_split)} fragmentos de texto.\n")

    # =====================================================================
    # 3. ENRIQUECIMIENTO CON IA (Extracción de Entidades)
    # =====================================================================
    # Aquí es donde ocurre la magia: le pedimos a una IA rápida (Flash)
    # que analice cada fragmento y extraiga datos clave para guardarlos
    # en la "etiqueta" (metadata) de cada fragmento.
    
    print("🏷️ Analizando fragmentos con IA para extraer entidades clave...")
    print("   (Este paso es más lento que una indexación normal, pero mucho más potente)\n")
    
    llm_extractor = ChatGoogleGenerativeAI(model=QUERY_MODEL, temperature=0)
    extraction_prompt = PromptTemplate.from_template(ENTITY_EXTRACTION_PROMPT)
    extraction_chain = extraction_prompt | llm_extractor

    for i, doc in enumerate(docs_split, 1):
        try:
            print(f"   [Fragmento {i}/{len(docs_split)}] Procesando...")
            
            # Ejecutamos la extracción de entidades
            resultado = extraction_chain.invoke({"text": doc.page_content})
            
            # Guardamos el resultado en un nuevo campo de metadatos
            # De esta forma, cada fragmento lleva "pegada" su propia ficha de datos
            doc.metadata["entidades_clave"] = resultado.content
            
        except Exception as e:
            print(f"   ⚠️ Error procesando fragmento {i}: {e}")
            doc.metadata["entidades_clave"] = "Error en extracción"

    print(f"\n✅ Análisis finalizado. Todos los fragmentos tienen metadatos enriquecidos.\n")

    # =====================================================================
    # 4. Crear Embeddings y almacenar en ChromaDB
    # =====================================================================
    print("🧠 Creando Embeddings y almacenando en ChromaDB...")
    
    embeddings_model = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

    if os.path.exists(CHROMA_DB_PATH):
        import shutil
        shutil.rmtree(CHROMA_DB_PATH)
        print("🗑️ Base de datos anterior eliminada para reconstrucción.")

    vectorstore = Chroma.from_documents(
        documents=docs_split,
        embedding=embeddings_model,
        persist_directory=CHROMA_DB_PATH
    )

    print(f"\n💾 Base de datos vectorial creada correctamente en: {CHROMA_DB_PATH}")
    print(f"📊 Total de vectores almacenados: {len(docs_split)}")
    print("\n✅ ¡Listo! Ahora puedes probar el asistente con: streamlit run app.py")


if __name__ == "__main__":
    build_vector_store()

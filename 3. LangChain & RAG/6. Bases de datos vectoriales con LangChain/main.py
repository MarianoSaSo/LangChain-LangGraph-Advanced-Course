import os
from dotenv import load_dotenv

# Dependencias necesarias de LangChain
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 1. Cargar las credenciales (API Key) correctamente
load_dotenv()

def main():
    print("🌟 Iniciando Lección de Bases de Datos Vectoriales con Chroma y Google Gemini...\n")

    # =====================================================================
    # 2. Cargar Documentos desde el directorio local
    # =====================================================================
    # Calculamos la ruta absoluta respecto a la ubicación de este archivo 'main.py'
    # para que funcione sin importar desde dónde lances el script.
    base_dir = os.path.dirname(__file__)
    directorio_contratos = os.path.join(base_dir, "contratos")
    
    print(f"📂 Cargando documentos PDF desde: {directorio_contratos}")
    
    loader = PyPDFDirectoryLoader(directorio_contratos)
    documentos = loader.load()

    print(f"✅ Se cargaron exitosamente {len(documentos)} documentos desde el directorio.\n")

    # =====================================================================
    # 3. Dividir Documentos en Chunks
    # =====================================================================
    # Creamos fragmentos pequeños para que la búsqueda semántica sea más precisa
    # y podamos inyectarla al contexto del LLM luego en RAG.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,   # Modificado a 1000 para que los fragmentos no sean demasiado grandes (mejor precisión)
        chunk_overlap=200
    )

    docs_split = text_splitter.split_documents(documentos)
    print(f"✂️ Se crearon {len(docs_split)} chunks (fragmentos) de texto a partir de los documentos base.\n")

    # =====================================================================
    # 4. Inicializar Google Embeddings y Crear/Conectar a Chroma
    # =====================================================================
    print("🧠 Creando Embeddings y almacenando en ChromaDB...")
    
    # Recuerda: usamos explícitamente el modelo validado en tu cuenta
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    # Creamos la base de datos vectorial apuntando al entorno local.
    # Si la carpeta 'chroma_db' no existe, la crea. Si ya existe, carga los datos.
    directorio_db = os.path.join(base_dir, "chroma_db")
    
    vectorstore = Chroma.from_documents(
        documents=docs_split,
        embedding=embeddings_model,
        persist_directory=directorio_db
    )
    print("💾 Base de datos vectorial persistida correctamente.\n")

    # =====================================================================
    # 5. Realizar Consultas de Similitud
    # =====================================================================
    consulta = "¿Dónde se encuentra el local del contrato en el que participa María Jiménez Campos?"
    print(f"❓ Consulta realizada: '{consulta}'")

    # Hacemos la llamada al similarity_search, pasando qué tan cerca queremos los datos (top K)
    resultados = vectorstore.similarity_search(consulta, k=2)

    print("\n" + "="*70)
    print("🎯 TOP DOS DOCUMENTOS MÁS SIMILARES RECUPERADOS OBTENIDOS:")
    print("="*70)
    
    for i, doc in enumerate(resultados, start=1):
        print(f"\n[{i}º Resultado Recuperado]")
        # Extraemos el contenido textual del fragmento
        print(f"📄 Fragmento de Texto:\n{doc.page_content.strip()}")
        # Extraemos la metadata (de qué archivo PDF provino y qué página)
        print(f"🏷️ Metadatos: {doc.metadata}")
        print("-" * 50)

if __name__ == "__main__":
    main()
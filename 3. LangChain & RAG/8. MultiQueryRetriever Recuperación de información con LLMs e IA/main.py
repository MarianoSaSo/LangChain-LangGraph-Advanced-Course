import os
from dotenv import load_dotenv

# Componentes de LangChain
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Cargar las credenciales (.env) correctamente
load_dotenv()

def main():
    print("🔍 Lección 8: MultiQueryRetriever con Google Gemini\n")
    
    # IMPORTANTE: Definir el LLM que se encargará de la reformulación
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0)

    # =====================================================================
    # 2. Conectar a la Base de Datos Existente
    # =====================================================================
    # Calculamos la ruta absoluta respecto a la ubicación de este archivo 'main.py'
    base_dir = os.path.dirname(__file__)
    
    # IMPORTANTE: Para que este script funcione tal cual, debemos apuntar a la base de datos que 
    # creamos en la lección anterior (Módulo 6). 
    # Usamos '../' para subir un nivel y entrar en la carpeta del Módulo 6.
    directorio_db_anterior = os.path.join(base_dir, "..", "6. Bases de datos vectoriales con LangChain", "chroma_db")
    
    # Debemos utilizar EXACTAMENTE EL MISMO modelo de embeddings con el que se creó la base de datos
    # En la lección 6 usamos 'models/gemini-embedding-001' de Google.
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    print(f"📡 Conectando a la base de datos vectorial en: {directorio_db_anterior}")
    
    # Cargamos la instancia de Chroma desde el disco (sin re-indexar nada)
    vectorstore = Chroma(
        persist_directory=directorio_db_anterior,
        embedding_function=embeddings_model
    )

    # =====================================================================
    # 3. Instanciar el Retriever
    # =====================================================================
    # En lugar de usar métodos específicos del VectorStore, lo elevamos a la abstracción de Retriever.
    # Esto nos permite cambiar el VectorStore en el futuro sin modificar el resto de la lógica de búsqueda.
    base_retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})
    retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)

    # =====================================================================
    # 4. Realizar la consulta usando la interfaz unificada (.invoke)
    # =====================================================================
    consulta = "¿Dónde se encuentra el local del contrato en el que participa María Jiménez Campos?"
    print(f"\n❓ Consulta realizada: '{consulta}'")

    # El método estándar de LangChain para recuperar información es 'invoke'
    # Este método nos devuelve una lista de objetos de tipo Document.
    resultados = retriever.invoke(consulta)

    print("\n" + "="*70)
    print("🎯 DOCUMENTOS RECUPERADOS OBTENIDOS VÍA RETRIEVER:")
    print("="*70)
    
    for i, doc in enumerate(resultados, start=1):
        print(f"\n[{i}º Resultado Recuperado]")
        # Extraemos el contenido textual del fragmento
        print(f"📄 Fragmento de Texto:\n{doc.page_content.strip()}")
        # Extraemos la metadata (fuente, página, etc.)
        print(f"🏷️ Metadatos: {doc.metadata}")
        print("-" * 50)

if __name__ == "__main__":
    main()

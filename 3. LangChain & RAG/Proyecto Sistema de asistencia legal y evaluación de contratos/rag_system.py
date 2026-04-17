# =================================================================
# RAG SYSTEM - Arquitectura principal del Sistema RAG
# =================================================================
# Este fichero implementa TODOS los componentes del sistema RAG:
# 1. Conexión al Vector Store (ChromaDB)
# 2. Definición de los modelos (consulta y generación)
# 3. Retriever con MMR + MultiQuery + Ensemble (híbrido)
# 4. Preprocesamiento de documentos (format_docs)
# 5. Cadena RAG completa con LCEL
# 6. Función de consulta (query_rag)
# =================================================================

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import EnsembleRetriever
import streamlit as st

# Importamos TODA la configuración y TODOS los prompts desde sus ficheros
from config import *
from prompts import *


# =================================================================
# FUNCIÓN PRINCIPAL: Inicialización del Sistema RAG
# =================================================================
# Decoramos con @st.cache_resource para que Streamlit NO recree
# todos estos componentes (clientes, cadenas) en cada interacción.
# Solo se ejecuta una vez y se reutiliza en memoria.
@st.cache_resource
def initialize_rag_system():
    """
    Define y conecta todos los componentes de la arquitectura RAG.
    Devuelve la cadena RAG lista para invocar y el retriever para inspección.
    """

    # -----------------------------------------------------------------
    # 1. VECTOR STORE - Conectar a la base de datos vectorial existente
    # -----------------------------------------------------------------
    # Importante: Usamos EXACTAMENTE el mismo modelo de embeddings con
    # el que se crearon los vectores en vector_store.py
    vectorstore = Chroma(
        embedding_function=GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL),
        persist_directory=CHROMA_DB_PATH
    )

    # -----------------------------------------------------------------
    # 2. MODELOS - Definimos dos LLMs con funciones distintas
    # -----------------------------------------------------------------
    # LLM para consultas (reformulación de preguntas en el MultiQueryRetriever)
    # Usamos temperatura 0 para que sea determinista en sus reformulaciones
    llm_queries = ChatGoogleGenerativeAI(model=QUERY_MODEL, temperature=0)

    # LLM para la generación final de la respuesta al usuario
    # Temperatura ligeramente más alta para respuestas naturales, no robóticas
    llm_generation = ChatGoogleGenerativeAI(model=GENERATION_MODEL, temperature=0.2)

    # -----------------------------------------------------------------
    # 3. RETRIEVER - Estrategia de recuperación de documentos
    # -----------------------------------------------------------------
    # Retriever base con MMR (Maximal Marginal Relevance)
    # MMR busca documentos relevantes PERO TAMBIÉN diversos entre sí,
    # evitando que devuelva 2 fragmentos casi idénticos.
    base_retriever = vectorstore.as_retriever(
        search_type=SEARCH_TYPE,
        search_kwargs={
            "k": SEARCH_K,
            "lambda_mult": MMR_DIVERSITY_LAMBDA,
            "fetch_k": MMR_FETCH_K
        }
    )
    #Arquitectura del sistema RAG parte 1
    # Retriever adicional por similitud de coseno (para el modo híbrido)
    similarity_retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": SEARCH_K}
    )

    # -----------------------------------------------------------------
    # 4. MULTI QUERY RETRIEVER con prompt personalizado
    # -----------------------------------------------------------------
    # Le damos al retriever un prompt especializado en derecho de arrendamiento,
    # para que genere variaciones inteligentes de la consulta del usuario.
    multi_query_prompt = PromptTemplate.from_template(MULTI_QUERY_PROMPT)

    mmr_multi_retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=llm_queries,
        prompt=multi_query_prompt
    )

    # -----------------------------------------------------------------
    # 5. ENSEMBLE RETRIEVER (Modo Híbrido) - Combina MMR + Similarity
    # -----------------------------------------------------------------
    # El Ensemble es el "mejor de dos mundos": combina la diversidad de MMR
    # con la precisión de la búsqueda por similitud de coseno.
    if ENABLE_HYBRID_SEARCH:
        ensemble_retriever = EnsembleRetriever(
            retrievers=[mmr_multi_retriever, similarity_retriever],
            weights=[0.7, 0.3]  # 70% peso a MMR, 30% a similitud
        )
        final_retriever = ensemble_retriever
    else:
        final_retriever = mmr_multi_retriever

    # -----------------------------------------------------------------
    # 6. PROMPT TEMPLATE para la generación final
    # -----------------------------------------------------------------
    prompt = PromptTemplate.from_template(RAG_TEMPLATE)

    # -----------------------------------------------------------------
    # 7. FUNCIÓN DE PREPROCESAMIENTO DE DOCUMENTOS
    # -----------------------------------------------------------------
    # Antes de pasar los fragmentos al LLM, los procesamos para:
    # - Añadir cabeceras con el número de fragmento
    # - Incluir metadatos (fuente, página) que ayudan al LLM a relacionar
    # - Separar claramente cada fragmento para evitar confusiones
    def format_docs(docs):
        formatted = []

        for i, doc in enumerate(docs, 1):
            # Cabecera: identifica el fragmento con su número
            header = f"[Fragmento {i}]"

            # Añadimos metadatos del documento si están disponibles
            if doc.metadata:
                # Extraemos el nombre del archivo fuente (sin la ruta completa)
                if 'source' in doc.metadata:
                    source = doc.metadata['source'].split("\\")[-1] if '\\' in doc.metadata['source'] else doc.metadata['source']
                    header += f" - Fuente: {source}"
                # Extraemos el número de página dentro del PDF original
                if 'page' in doc.metadata:
                    header += f" - Página: {doc.metadata['page']}"

            # Contenido limpio del fragmento
            content = doc.page_content.strip()
            formatted.append(f"{header}\n{content}")

        # Devolvemos todos los fragmentos concatenados, separados con doble salto de línea
        return "\n\n".join(formatted)

    # -----------------------------------------------------------------
    # 8. CADENA RAG COMPLETA (LCEL)
    # -----------------------------------------------------------------
    # Esta es la pieza central: conecta TODO usando el operador pipe (|)
    #
    # Flujo: Pregunta del usuario
    #   → "context": retriever obtiene fragmentos → format_docs los preprocesa
    #   → "question": RunnablePassthrough() pasa la pregunta tal cual
    #   → prompt: inyecta context y question en la plantilla
    #   → llm_generation: genera la respuesta
    #   → StrOutputParser: extrae el texto limpio
    rag_chain = (
        {
            "context": final_retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm_generation
        | StrOutputParser()
    )

    # Devolvemos dos objetos en una tupla: la cadena completa y el retriever específico.
    # NOTA PARA ALUMNOS: mmr_multi_retriever es el segundo objeto que enviamos.
    return rag_chain, mmr_multi_retriever


# =================================================================
# FUNCIÓN DE CONSULTA: Invoca la cadena RAG
# =================================================================
def query_rag(question):
    """
    Recibe la pregunta del usuario, invoca la cadena RAG completa
    y devuelve la respuesta junto con los documentos utilizados.
    """
    try:
        # DESEMPAQUETADO: Aquí recibimos los dos objetos que devuelve 'initialize_rag_system'.
        # 'retriever' aquí es el mismo objeto que dentro llamamos 'mmr_multi_retriever'.
        # El nombre cambia al recibirlo, pero el objeto (el motor de búsqueda) es el mismo.
        rag_chain, retriever = initialize_rag_system()

        # Ejecutamos la cadena RAG completa con la pregunta del usuario
        response = rag_chain.invoke(question)

        # Obtenemos los documentos relevantes para mostrarlos en la UI
        docs = retriever.invoke(question)

        # Formateamos la información de cada documento para Streamlit
        docs_info = []
        for i, doc in enumerate(docs[:SEARCH_K], 1):
            doc_info = {
                "fragmento": i,
                "contenido": doc.page_content[:1000] + "..." if len(doc.page_content) > 1000 else doc.page_content,
                "fuente": doc.metadata.get('source', 'No especificada').split("\\")[-1],
                "pagina": doc.metadata.get('page', 'No especificada')
            }
            docs_info.append(doc_info)

        return response, docs_info

    except Exception as e:
        error_msg = f"Error al procesar la consulta: {str(e)}"
        return error_msg, []


# =================================================================
# FUNCIÓN AUXILIAR: Información del Retriever para Streamlit
# =================================================================
def get_retriever_info():
    """Obtiene información sobre la configuración actual del retriever."""
    return {
        "tipo": f"{SEARCH_TYPE.upper()} + MultiQuery" + (" + Hybrid" if ENABLE_HYBRID_SEARCH else ""),
        "documentos": SEARCH_K,
        "diversidad": MMR_DIVERSITY_LAMBDA,
        "candidatos": MMR_FETCH_K,
        "umbral": SIMILARITY_THRESHOLD if ENABLE_HYBRID_SEARCH else "N/A"
    }
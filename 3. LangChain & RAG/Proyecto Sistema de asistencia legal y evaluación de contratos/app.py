# =================================================================
# APP.PY - Interfaz Gráfica del Asistente Legal RAG (Streamlit)
# =================================================================
# Este archivo implementa la UI de nuestra aplicación.
# Para ejecutarlo: streamlit run app.py
# =================================================================

import streamlit as st
from dotenv import load_dotenv, find_dotenv
from rag_system import query_rag, get_retriever_info
from config import QUERY_MODEL, GENERATION_MODEL

# Cargar las variables de entorno (.env) con la GOOGLE_API_KEY
load_dotenv(find_dotenv())

# -----------------------------------------------------------------
# Configuración de la página
# -----------------------------------------------------------------
st.set_page_config(
    page_title="Sistema RAG - Asistente Legal",
    page_icon="⚖️",
    layout="wide"
)

# Título
st.title("⚖️ Sistema RAG - Asistente Legal")
st.divider()

# Inicializar el historial de chat en session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------------------------------
# Sidebar - Información del sistema
# -----------------------------------------------------------------
with st.sidebar:
    st.header("📋 Información del Sistema")

    # Información del retriever (obtenida dinámicamente desde config)
    retriever_info = get_retriever_info()

    st.markdown("**🔍 Retriever:**")
    st.info(f"Tipo: {retriever_info['tipo']}")

    st.markdown("**🤖 Modelos (Google Gemini):**")
    st.info(f"Consultas: {QUERY_MODEL}\nRespuestas: {GENERATION_MODEL}")

    st.divider()

    if st.button("🗑️ Limpiar Chat", type="secondary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -----------------------------------------------------------------
# Layout principal con dos columnas
# -----------------------------------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Chat")

    # Mostrar historial de mensajes
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

with col2:
    st.markdown("### 📄 Documentos Relevantes")

    # Mostrar documentos utilizados en la última respuesta
    if st.session_state.messages:
        last_message = st.session_state.messages[-1]
        if last_message["role"] == "assistant" and "docs" in last_message:
            docs = last_message["docs"]

            if docs:
                for doc in docs:
                    with st.expander(f"📄 Fragmento {doc['fragmento']}", expanded=False):
                        st.markdown(f"**Fuente:** {doc['fuente']}")
                        st.markdown(f"**Página:** {doc['pagina']}")
                        st.markdown("**Contenido:**")
                        st.text(doc['contenido'])

# -----------------------------------------------------------------
# Input del usuario
# -----------------------------------------------------------------
if prompt := st.chat_input("Escribe tu consulta sobre contratos de arrendamiento..."):
    # Añadir mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generar respuesta invocando la cadena RAG
    with st.spinner("🔍 Analizando contratos..."):
        response, docs = query_rag(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response, "docs": docs})

    # Recargar para mostrar los nuevos mensajes
    st.rerun()

# -----------------------------------------------------------------
# Footer
# -----------------------------------------------------------------
st.divider()
st.markdown(
    "<div style='text-align: center; color: #666;'>🏛️ Asistente Legal RAG con Google Gemini + MMR Retriever</div>",
    unsafe_allow_html=True
)
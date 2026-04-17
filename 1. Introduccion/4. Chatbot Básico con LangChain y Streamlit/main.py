# --- IMPORTACIONES ---
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Cargamos las variables de entorno para que el sistema reconozca la OPENAI_API_KEY
# Este paso es fundamental para que la aplicación tenga acceso al modelo de IA
load_dotenv()

# --- CONFIGURACIÓN DE LA INTERFAZ (UI) ---
# Definimos los parámetros estéticos de la pestaña y el cuerpo de la aplicación
st.set_page_config(
    page_title="Chatbot Básico | Tutorial", 
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Chatbot Básico con LangChain")
st.markdown("""
    Bienvenido a este chatbot educativo. Aquí aprenderás a usar:
    1. **LangChain** para la lógica de IA.
    2. **Streamlit** para la interfaz visual.
    3. **LCEL** (LangChain Expression Language) para conectar componentes.
""")

# --- CONFIGURACIÓN EN LA BARRA LATERAL (SIDEBAR) ---
# Usamos el sidebar para que los ajustes no estorben en la conversación principal
with st.sidebar:
    st.header("⚙️ Ajustes del Modelo")
    # La temperatura controla la "creatividad" del modelo (0 = preciso, 1 = creativo)
    temp = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    # Lista desplegable para que el usuario elija el motor de IA
    model = st.selectbox("Modelo", ["gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"])
    
    # Creamos la instancia del modelo de chat con los parámetros seleccionados
    chat_model = ChatOpenAI(model=model, temperature=temp)

# --- GESTIÓN DE LA MEMORIA (SESSION STATE) ---
# Streamlit se reinicia en cada interacción. st.session_state es como un "diccionario" 
# que sobrevive a los reinicios, permitiéndonos guardar el historial de mensajes.
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# --- DISEÑO DEL PROMPT (PROMPT TEMPLATE) ---
# Los Prompt Templates son moldes que estructuran la información que le enviamos a la IA.
# Aquí definimos la "personalidad" del asistente y cómo debe leer el historial.
p_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""Eres un asistente útil y amigable llamado ChatBot Pro. 

    Historial de conversación (Contexto):
    {historial}

    Pregunta actual del usuario: {mensaje}
    Respuesta:"""
)

# --- CONSTRUCCIÓN DE LA CADENA (LCEL) ---
# Usamos el operador '|' para conectar el template con el modelo. 
# Esto crea una "tubería" donde el texto pasa por el molde y luego al motor de IA.
cadena = p_template | chat_model

# --- RENDERIZADO DEL CHAT (DIBUJAR MENSAJES) ---
# Recorremos la lista de mensajes en memoria para dibujarlos en pantalla.
# st.chat_message crea las burbujas de texto diferenciadas para 'user' y 'assistant'.
for msg in st.session_state.mensajes:
    # Usamos isinstance para saber si el mensaje es del usuario o de la IA
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# Botón para limpiar el chat reiniciando la variable de mensajes
if st.button("🗑️ Borrar Conversación"):
    st.session_state.mensajes = []
    st.rerun()

# --- LÓGICA DE INTERACCIÓN ---
# st.chat_input crea una caja de texto al final de la página.
# El condicional 'if pregunta:' solo se activa cuando el usuario pulsa Enter.
if pregunta := st.chat_input("Escribe tu duda aquí..."):
    # 1. Mostramos el mensaje del usuario inmediatamente
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    # 2. Lógica para generar y mostrar la respuesta de la IA
    try:
        with st.chat_message("assistant"):
            # st.empty() crea un espacio vacío que iremos rellenando poco a poco
            res_placeholder = st.empty()
            full_res = ""

            # STREAMING: En lugar de esperar a que la IA termine toda la frase,
            # vamos recibiendo "chunks" (trozos) de texto para que se sienta más rápido.
            # Pasamos el mensaje actual y el historial completo para que tenga contexto.
            for chunk in cadena.stream({"mensaje": pregunta, "historial": st.session_state.mensajes}):
                full_res += chunk.content
                # Añadimos un cursor visual '▌' mientras la IA "escribe"
                res_placeholder.markdown(full_res + "▌")
            
            # Al terminar, quitamos el cursor y dejamos el texto final
            res_placeholder.markdown(full_res)
        
        # 3. Guardamos ambos mensajes en el historial (memoria) para el siguiente turno
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_res))
        
    except Exception as e:
        # Mostramos un error amigable si algo falla (ej: falta de saldo o mala conexión)
        st.error(f"⚠️ Error técnico: {str(e)}")
        st.info("Asegúrate de tener tu archivo .env configurado con una API Key válida.")

# --- INSTRUCCIONES DE LANZAMIENTO ---
# Para ejecutar esta aplicación, abre tu terminal y escribe:
# streamlit run main.py

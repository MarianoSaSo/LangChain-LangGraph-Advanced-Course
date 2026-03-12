# Importamos la clase principal para conectar con los modelos de OpenAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Importamos los esquemas de mensajes:
# SystemMessage: Instrucciones de fondo para el modelo.
# HumanMessage: Lo que el usuario envía.
# AIMessage: La respuesta que genera la inteligencia artificial.
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# Importamos Streamlit, que nos permite crear la interfaz visual con Python
import streamlit as st


# --- CONFIGURACIÓN DE LA INTERFAZ ---
# Cargamos la configuración de las variables de entorno (.env) que está en la raíz
# Esto carga tu API_KEY del archivo .env
load_dotenv()

# Definimos los metadatos que se verán en la pestaña del navegador
st.set_page_config(
    page_title="Chatbot con LangChain y Streamlit",
    page_icon="🤖",
    layout="centered" # Cambiado a centered para que el chat se vea mejor alineado
)

# Mostramos el título principal y un texto introductorio
st.title("🤖 Asistente Virtual con LangChain")
st.markdown("""
    Bienvenido a este chatbot interactivo fabricado con **LangChain** y **Streamlit**. 
    ¡Escribe un mensaje en el cuadro inferior para comenzar la conversación!
""")


# --- CONFIGURACIÓN DEL MODELO ---
# Inicializamos el objeto del modelo que vamos a utilizar.
# gpt-4o-mini: Un modelo equilibrado en potencia y eficiencia.
# temperature=0: Hace que las respuestas sean más precisas y menos aleatorias.
chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# Crear el historial de memoria
# Guardaremos los mensajes en el diccionario session state de streamlit
#Inicializamos el historial de memoria
if "messages" not in st.session_state:
    #Si no existe, lo creamos como una lista vacía
    st.session_state.messages = []
#En el caso de que ya haya mensajes querra decir que ya hemos interactuado con el chat
#Mostrar mensajes previos en la interfaz
for message in st.session_state.messages:
    if isinstance(message, SystemMessage):
        #No hagas nada\
        continue
    role = "assistant" if isinstance(message, AIMessage) else "user"
    st.chat_message(role).write(message.content)

    
#Campo de entrada del usuario
question = st.chat_input("¿En qué puedo ayudarte?")
if question:
    #Mostrar el mensaje del usuario en la interfaz
    with st.chat_message("user"):
        st.markdown(question)

    #Almacenamos el mensaje del usuario en la memoria de la sesion
    st.session_state.messages.append(HumanMessage(content=question))

    #Generar la respuesta usando el modelo de lenguaje
    respuesta = chat_model.invoke(st.session_state.messages)

    #Mostrar la respuesta en la interfaz
    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    #Almacenamos la respuesta en la memoria de la sesion
    st.session_state.messages.append(AIMessage(content=respuesta.content))  







### Para arrancar la app ###
# -> streamlit run "1. Introduccion/4. Chatbot Básico con LangChain y Streamlit/main.py"
# ->streamlit run main.py


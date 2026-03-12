import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# =================================================================
# LECCIÓN 1: INTRODUCCIÓN A LANGCHAIN - HOLA MUNDO
# =================================================================

# 1. Cargar las variables de entorno desde el archivo .env
# Este paso es fundamental para que LangChain pueda acceder a nuestras API Keys
# sin que estas queden expuestas directamente en el código fuente.
# NOTA: Debes tener un archivo .env en la raíz del proyecto con OPENAI_API_KEY=tu_clave
load_dotenv()

# 2. Inicializar el modelo de lenguaje (LLM)
# Utilizamos ChatOpenAI, que es la interfaz de LangChain para los modelos de OpenAI.
# Argumentos clave:
# - model_name: Usamos "gpt-4o-mini" (rápido y económico para pruebas).
# - temperature: Define la creatividad (0 es determinista, ideal para este curso).
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# 3. Preparar nuestra pregunta (Prompt)
# En LangChain, la forma más básica de interactuar con el modelo es enviándole un texto.
pregunta = "¿En qué año llegó el hombre a la luna?"

# 4. Invocar al modelo (Invoke)
# El método .invoke() es el estándar en LangChain para enviar una petición a la API.
# Este método bloquea la ejecución hasta recibir la respuesta.
print(f"--- Pregunta de ejemplo: {pregunta} ---\n")

try:
    # Llamamos al modelo
    response = llm.invoke(pregunta)
    
    # 5. Mostrar la respuesta
    # El objeto retornado no es solo texto, sino un objeto AIMessage que contiene:
    # - content: El texto de la respuesta.
    # - response_metadata: Información técnica (tokens usados, tiempo, etc).
    print("--- Respuesta del modelo ---")
    print(response.content)
    
except Exception as e:
    print(f"ERROR: No se pudo conectar con el modelo. Verifica tus API Keys en el archivo .env.\n{e}")
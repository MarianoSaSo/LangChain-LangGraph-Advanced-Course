import os
from dotenv import load_dotenv, find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# =================================================================
# LECCIÓN 2: HOLA MUNDO CON GOOGLE GEMINI
# =================================================================

# 1. Cargar las variables de entorno (.env)
# find_dotenv() busca el archivo en la raíz del proyecto automáticamente
load_dotenv(find_dotenv())

# 2. Inicializar el modelo de Google
# Model: "gemini-1.5-flash" es el recomendado por su velocidad
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# 3. Datos de la interacción
pregunta = "En qué año llegó el hombre a la luna?"
print(f"--- Pregunta de la lección: {pregunta} ---\n")

try:
    # 4. Invocación al modelo (método estándar de LangChain)
    response = llm.invoke(pregunta)
    
    # 5. Mostrar resultado
    print("--- Respuesta de Google Gemini ---")
    print(response.content)
    
except Exception as e:
    print(f"ERROR: No se pudo conectar con Gemini. Verifica tu API Key.\n{e}")

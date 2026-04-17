import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# 1. Cargar variables de entorno (API Key de OpenAI)
load_dotenv()

# 2. Configuración (Simulando lo que antes tomábamos de Streamlit)
temperature = 0.5
model_name = "gpt-3.5-turbo"
personalidad = "Útil y amigable"

# 3. Diccionario de personalidades
system_messages = {
    "Útil y amigable": "Eres un asistente útil y amigable llamado ChatBot Pro. Responde de manera clara y concisa.",
    "Profesional y formal": "Eres un asistente profesional y formal. Proporciona respuestas precisas y bien estructuradas.",
    "Casual y relajado": "Eres un asistente casual y relajado. Habla de forma natural y amigable, como un buen amigo.",
    "Experto técnico": "Eres un asistente experto técnico. Proporciona respuestas detalladas con precisión técnica.",
    "Creativo y divertido": "Eres un asistente creativo y divertido. Usa analogías, ejemplos creativos y mantén un tono alegre."
}

# 4. Crear el modelo de chat
chat_model = ChatOpenAI(model=model_name, temperature=temperature)

# 5. Configurar el ChatPromptTemplate con la personalidad elegida
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system_messages[personalidad]),
    ("human", "Historial de conversación:\n{historial}\n\nPregunta actual: {mensaje}")
])

# 6. Unir el Prompt y el Modelo creando una cadena (LCEL)
cadena = chat_prompt | chat_model

# 7. Ejecutar una prueba simple en la consola para comprobar que funciona
if __name__ == "__main__":
    pregunta = "¿Qué es LangChain?"
    historial_simulado = "(No hay historial previo)"
    
    print(f"Personalidad seleccionada: {personalidad}")
    print(f"Modelo: {model_name} | Temperatura: {temperature}\n")
    print("-" * 50)
    print(f"Usuario: {pregunta}")
    print("Asistente: ", end="", flush=True)

    # Ocupamos stream() de la cadena tal como lo hacíamos en main.py para mostrar a trozos
    for chunk in cadena.stream({"mensaje": pregunta, "historial": historial_simulado}):
        print(chunk.content, end="", flush=True)
        
    print("\n" + "-" * 50)

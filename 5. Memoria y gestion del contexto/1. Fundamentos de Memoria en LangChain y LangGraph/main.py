import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Cargar variables de entorno (API Keys)
load_dotenv()

# 1. INSTANCIACIÓN DEL MODELO
# Usamos GPT-4o-mini por su eficiencia en coste y velocidad
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 2. DEFINICIÓN DE LA PLANTILLA (PROMPT TEMPLATE)
# El "MessagesPlaceholder" es la clave aquí: reserva un espacio dinámico para el historial
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil y amable."),
    MessagesPlaceholder(variable_name="historial"), # Aquí se inyectará la lista de mensajes previos
    ("human", "{input}")
])

# 3. CREACIÓN DE LA CADENA (CHAIN)
# Unimos el prompt con el modelo usando LCEL (LangChain Expression Language)
chain = prompt_template | llm

# 4. GESTIÓN MANUAL DE LA MEMORIA
# Creamos una lista vacía para almacenar los objetos de mensaje (HumanMessage y AIMessage)
history = []

print("--- Chat en terminal (escribe 'Salir' para terminar) ---")

# 5. BUCLE PRINCIPAL DE INTERACCIÓN
try:
    while True:
        # Solicitar entrada al usuario
        user_input = input("\nUsuario: ")

        # Condición de salida
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("Cerrando el chat. ¡Hasta pronto!")
            break

        # INVOCACIÓN DE LA CADENA
        # Pasamos el input actual y todo el historial acumulado hasta el momento
        respuesta = chain.invoke({
            "input": user_input,
            "historial": history
        })

        # Mostrar respuesta del asistente
        print(f"Asistente: {respuesta.content}")

        # ACTUALIZACIÓN DEL HISTORIAL
        # Para que el LLM "recuerde" en la siguiente iteración, debemos guardar ambos mensajes anadiendolos a la lista de mensajes.
        history.extend([
            HumanMessage(content=user_input),
            AIMessage(content=respuesta.content)
        ])

except KeyboardInterrupt:
    print("\nInterrupción detectada. Cerrando...")

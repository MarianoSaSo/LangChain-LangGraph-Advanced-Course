import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# Cargar API Keys
load_dotenv()

# 1. MODELO Y PROMPT (IGUAL QUE EN LA LECCIÓN ANTERIOR)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil."),
    MessagesPlaceholder(variable_name="history"), # Este nombre debe coincidir con history_messages_key más abajo
    ("human", "{input}")
])

chain = prompt | llm

# 2. ALMACÉN DE HISTORIALES (STORE)
# Este diccionario actuará como nuestra "base de datos" temporal en RAM
store = {}

# 3. FUNCIÓN PARA GESTIONAR SESIONES
# Esta función es obligatoria para RunnableWithMessageHistory
def get_session_history(session_id: str):
    """
    Recupera el historial de una sesión existente o crea uno nuevo si no existe.
    Nota: Se utiliza 'InMemoryChatMessageHistory', por lo que los datos se pierden al cerrar el programa.
    """
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 4. CREACIÓN DE LA CADENA CON MEMORIA AUTOMÁTICA
# RunnableWithMessageHistory envuelve nuestra cadena original y gestiona el historial por nosotros
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",      # La variable del prompt que contiene el mensaje del usuario
    history_messages_key="history"   # La variable del prompt (Placeholder) donde se inyectará el historial
)

print("--- Chat con RunnableWithMessageHistory (Nativo de LangChain) ---")
print("Escribe 'salir' para terminar\n")

# Identificador de sesión (en una app real, esto sería único por usuario/chat)
session_id = "sesion_maniek_01"

while True:
    try:
        user_input = input("Tú: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nHasta luego!")
        break

    if not user_input:
        continue
        
    if user_input.lower() in {"salir", "exit", "quit"}:
        print("Hasta luego!")
        break

    # 5. INVOCACIÓN CON CONFIGURACIÓN DE SESIÓN
    # Ya no pasamos el historial manualmente. Solo pasamos el input y el config con el session_id.
    respuesta = chain_with_memory.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}
    )
    
    print(f"Asistente: {respuesta.content}")

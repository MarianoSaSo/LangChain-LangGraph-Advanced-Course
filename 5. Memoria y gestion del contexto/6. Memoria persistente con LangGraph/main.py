"""
=============================================================================
LECCIÓN 6: Memoria persistente con LangGraph (SqliteSaver)
=============================================================================

Diferencia con la lección 3 (MemorySaver):
  - Lección 3: historial en RAM → se pierde al cerrar el programa.
  - Lección 6: historial en disco (historial.db) → sobrevive al cerrar y volver a ejecutar.

Teoría: Teoria_Memoria_Persistente_LangGraph.md
"""
from pathlib import Path

import sqlite3
from dotenv import find_dotenv, load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, MessagesState, StateGraph

load_dotenv(find_dotenv())

# ---------------------------------------------------------------------------
# Dónde se guarda la base de datos
# ---------------------------------------------------------------------------
# Path absoluto en la carpeta de ESTA lección (no en la raíz del curso).
# Si el archivo no existe, sqlite3 lo crea en la primera ejecución.
CARPETA_LECCION = Path(__file__).resolve().parent
RUTA_BASE_DATOS = CARPETA_LECCION / "historial.db"

# ---------------------------------------------------------------------------
# Identificador de conversación (thread_id)
# ---------------------------------------------------------------------------
# Mismo valor en dos ejecuciones distintas del programa = misma conversación.
# Cambia este string (p. ej. "sesion_terminal_2") para empezar un chat vacío.
THREAD_ID = "sesion_Maniek_02"


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

workflow = StateGraph(MessagesState)


def chatbot_node(state: MessagesState):
    """Igual que en la lección 3: un nodo que llama al LLM con el historial del estado."""
    system_prompt = "Eres un asistente amigable que recuerda conversaciones previas."
    messages_for_llm = [SystemMessage(content=system_prompt)] + list(state["messages"])
    response = llm.invoke(messages_for_llm)
    return {"messages": [response]}


workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

# ---------------------------------------------------------------------------
# CHECKPOINTER PERSISTENTE (cambio principal respecto a MemorySaver)
# ---------------------------------------------------------------------------
# 1) sqlite3.connect → conexión al fichero .db en disco.
#    check_same_thread=False permite usar la misma conexión desde Streamlit/hilos;
#    en este script de terminal también es el patrón del curso (Helpdesk).
#
# 2) SqliteSaver(conn) → implementación de checkpointer que guarda snapshots
#    del estado del grafo (incluido messages) en tablas SQLite.
#
# 3) compile(checkpointer=memory) → mismo sitio que con MemorySaver; solo cambia
#    la clase del checkpointer.
conn = sqlite3.connect(str(RUTA_BASE_DATOS), check_same_thread=False)
memory = SqliteSaver(conn)
app = workflow.compile(checkpointer=memory)


def chat(message: str, thread_id: str = THREAD_ID) -> str:
    """
    Invoca el grafo con un mensaje nuevo del usuario.

    config["configurable"]["thread_id"]:
      Clave que LangGraph usa para separar conversaciones en la base de datos.
      Mismo thread_id → recupera el historial guardado en historial.db.
    """
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"messages": [HumanMessage(content=message)]}, config)
    return result["messages"][-1].content


if __name__ == "__main__":
    print("=== 6. Memoria persistente (SqliteSaver) ===")
    print(f"Base de datos: {RUTA_BASE_DATOS}")
    print(f"thread_id actual: {THREAD_ID}")
    print("(Cambia THREAD_ID en main.py para un chat nuevo sin historial previo.)\n")
    print("Escribe 'salir' para terminar.\n")

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

        respuesta = chat(user_input, thread_id=THREAD_ID)
        print(f"Asistente: {respuesta}\n")

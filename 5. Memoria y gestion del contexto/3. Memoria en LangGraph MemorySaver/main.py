"""
Chat en terminal con memoria usando LangGraph.

Lee la teoría en: Teoria_Memoria_LangGraph_MemorySaver.md
"""
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph

# ---------------------------------------------------------------------------
# 0. Variables de entorno (API key)
# ---------------------------------------------------------------------------
# Subimos dos carpetas desde esta lección hasta la raíz del curso, donde suele
# estar el archivo .env con OPENAI_API_KEY (igual que en otras unidades).
_curso_raiz = Path(__file__).resolve().parents[2]
load_dotenv(_curso_raiz / ".env")
load_dotenv()

# ---------------------------------------------------------------------------
# 1. Modelo de lenguaje
# ---------------------------------------------------------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ---------------------------------------------------------------------------
# 2. Grafo (StateGraph) y tipo de estado (MessagesState)
# ---------------------------------------------------------------------------
# - StateGraph: "lienzo" donde registras nodos (funciones) y aristas (flechas).
# - MessagesState: estado predefinido para chat; incluye la clave "messages",
#   una lista con el historial (humano, asistente, etc.).
#   No hace falta que los alumnos definan a mano un TypedDict para este caso.
workflow = StateGraph(MessagesState)


def chatbot_node(state: MessagesState):
    """
    Nodo único del grafo: lee el historial del estado, llama al LLM y devuelve
    solo la nueva respuesta del asistente.

    LangGraph se encarga de fusionar ese retorno con el estado anterior. En
    MessagesState, la lista "messages" está preparada para ir acumulando
    turnos (no sustituye todo el historial por una sola respuesta).
    """
    system_prompt = "Eres un asistente amigable que recuerda conversaciones previas."
    # Orden típico: instrucciones del sistema primero, luego todo lo conversado.
    messages_for_llm = [SystemMessage(content=system_prompt)] + list(state["messages"])
    response = llm.invoke(messages_for_llm)
    return {"messages": [response]}


workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
# Con un solo nodo el grafo podría terminar sin arista a END; la añadimos para
# que el diagrama mental sea completo: START → chatbot → END.
workflow.add_edge("chatbot", END)

# ---------------------------------------------------------------------------
# 3. Checkpointer en RAM: MemorySaver
# ---------------------------------------------------------------------------
# Un "checkpoint" guarda una instantánea del estado al avanzar el grafo.
# MemorySaver guarda esas instantáneas en memoria del proceso (se pierde al
# cerrar el programa o apagar el ordenador). Para persistencia en disco se
# usa otro checkpointer (p. ej. SQLite), tema que veréis más adelante.
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def chat(message: str, thread_id: str = "sesion_terminal") -> str:
    """
    Función auxiliar tipo "enviar un mensaje al chat".

    - thread_id: identifica la conversación (equivalente conceptual al
      session_id de RunnableWithMessageHistory). Mismo thread_id ⇒ mismo
      historial recuperado por el checkpointer.
    """
    config = {"configurable": {"thread_id": thread_id}}
    # Cada turno aporta un nuevo mensaje humano; el grafo recupera el estado
    # previo del mismo thread_id y concatena la conversación.
    result = app.invoke({"messages": [HumanMessage(content=message)]}, config)
    last = result["messages"][-1]
    return last.content


if __name__ == "__main__":
    print("Chat en terminal (escribe 'salir' para terminar)\n")
    session_id = "sesion_Maniek_01"

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

        respuesta = chat(user_input, session_id)
        print("Asistente:", respuesta)

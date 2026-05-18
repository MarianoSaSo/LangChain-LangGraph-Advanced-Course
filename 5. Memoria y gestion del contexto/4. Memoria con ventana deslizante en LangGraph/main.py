"""
Chat en terminal con memoria de ventana deslizante (LangGraph + trim_messages).

- El checkpointer guarda TODO el historial en RAM.
- Antes de llamar al LLM, recortamos a los últimos N mensajes con trim_messages.

Teoría: Teoria_Memoria_Ventana_Deslizante.md
"""
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, trim_messages
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph

# ---------------------------------------------------------------------------
# 0. Variables de entorno
# ---------------------------------------------------------------------------
_curso_raiz = Path(__file__).resolve().parents[2]
load_dotenv(_curso_raiz / ".env")
load_dotenv()

# ---------------------------------------------------------------------------
# 1. Ajustes de la ventana deslizante
# ---------------------------------------------------------------------------
# Cada "token" del trimmer cuenta como 1 mensaje completo (ver token_counter=len).
# Con max_tokens=4 el modelo ve como máximo los 4 últimos mensajes del historial
# (más el SystemMessage que añadimos aparte en el nodo).
MAX_MENSAJES_EN_VENTANA = 4

SYSTEM_PROMPT = "Eres un asistente amigable que recuerda conversaciones recientes."

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ---------------------------------------------------------------------------
# 2. Estado: WindowedState (mismo contenido que MessagesState, nombre distinto)
# ---------------------------------------------------------------------------
# Heredar de MessagesState sin añadir campos documenta en el código que usamos
# ventana deslizante. El grafo sigue teniendo la clave "messages".
class WindowedState(MessagesState):
    """Estado de chat; mismo esquema que MessagesState, nombre semántico para esta lección."""


# ---------------------------------------------------------------------------
# 3. Trimmer: recortar historial antes de enviarlo al LLM
# ---------------------------------------------------------------------------
# trim_messages es de langchain_core.messages (no confundir con "trim" genérico).
trimmer = trim_messages(
    strategy="last",           # Quedarse con los últimos N "tokens"
    max_tokens=MAX_MENSAJES_EN_VENTANA,
    token_counter=len,         # Cada mensaje cuenta como 1 token → ventana de N mensajes
    start_on="human",          # El recorte empieza en un mensaje de usuario (recomendado)
    include_system=True,       # Si hubiera SystemMessage en state["messages"], conservarla
)

workflow = StateGraph(WindowedState)


def chatbot_node(state: WindowedState):
    """
    1) Recorta state["messages"] con el trimmer (solo para el LLM).
    2) Añade el prompt de sistema y llama al modelo.
    3) Devuelve la nueva respuesta; LangGraph la concatena al historial COMPLETO del estado.

    Importante: en memoria (MemorySaver) sigue guardándose todo el historial;
    el recorte no borra mensajes antiguos del checkpoint, solo limita lo que ve el LLM.
    """
    trimmed_messages = trimmer.invoke(state["messages"])
    messages_for_llm = [SystemMessage(content=SYSTEM_PROMPT)] + list(trimmed_messages)
    response = llm.invoke(messages_for_llm)
    return {"messages": [response]}


workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def chat(message: str, thread_id: str = "sesion_terminal") -> str:
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"messages": [HumanMessage(content=message)]}, config)
    return result["messages"][-1].content


if __name__ == "__main__":
    print("--- Chat con ventana deslizante (LangGraph + trim_messages) ---")
    print(f"Ventana: últimos {MAX_MENSAJES_EN_VENTANA} mensajes hacia el LLM.")
    print("Escribe 'salir' para terminar.\n")

    session_id = "sesion_terminal"

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
        print(f"Asistente: {respuesta}\n")

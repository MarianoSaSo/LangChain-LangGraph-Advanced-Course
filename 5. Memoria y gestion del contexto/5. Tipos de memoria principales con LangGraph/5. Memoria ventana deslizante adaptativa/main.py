"""
Estrategia 5: Ventana deslizante adaptativa.

El tamaño de ventana cambia según palabras clave en mensajes recientes
(código, historia, mensajes muy largos). Ver calculate_adaptive_window_size en el artículo.

Artículo: ../Teoria_Tipos_Memoria_LangGraph.md
"""
from dotenv import find_dotenv, load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, START, StateGraph

load_dotenv(find_dotenv())

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
workflow = StateGraph(MessagesState)


def calculate_adaptive_window_size(messages: list[BaseMessage]) -> int:
    """Del artículo: ventana base 6 con ajustes por contexto."""
    base_size = 6
    if not messages:
        return base_size

    last3 = messages[-3:]
    last2 = messages[-2:]

    if any("código" in (getattr(m, "content", "") or "").lower() for m in last3):
        return base_size + 4
    if any("historia" in (getattr(m, "content", "") or "").lower() for m in last2):
        return base_size + 6
    if any(len(getattr(m, "content", "") or "") > 500 for m in last2):
        return max(2, base_size - 2)
    return base_size


def adaptive_sliding_window(messages: list[BaseMessage]) -> list[BaseMessage]:
    window_size = calculate_adaptive_window_size(messages)
    if len(messages) <= window_size:
        return list(messages)
    return messages[-window_size:]


def chatbot_node(state: MessagesState):
    all_messages = list(state["messages"])
    window_size = calculate_adaptive_window_size(all_messages)
    messages_for_llm = adaptive_sliding_window(all_messages)
    system = SystemMessage(
        content=f"Eres un asistente útil. (Ventana adaptativa actual: {window_size} mensajes al LLM.)"
    )
    response = llm.invoke([system] + messages_for_llm)
    return {"messages": [response]}


workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)
app = workflow.compile(checkpointer=MemorySaver())


def chat(text: str, thread_id: str = "sesion_adaptativa") -> str:
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"messages": [HumanMessage(content=text)]}, config)
    return result["messages"][-1].content


if __name__ == "__main__":
    print("=== 5. Ventana deslizante adaptativa ===")
    print("Prueba mensajes con 'código' o 'historia' y observa el tamaño de ventana.\n")
    tid = "sesion_adaptativa"
    while True:
        try:
            user = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user or user.lower() in {"salir", "exit", "quit"}:
            print("Hasta luego.")
            break
        print("Asistente:", chat(user, tid), "\n")

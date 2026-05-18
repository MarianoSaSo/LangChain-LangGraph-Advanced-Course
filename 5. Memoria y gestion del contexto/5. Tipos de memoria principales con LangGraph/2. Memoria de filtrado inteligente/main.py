"""
Estrategia 2: Memoria de filtrado inteligente.

Mantiene mensajes "importantes" (palabras clave, largos, System) + 4 regulares recientes.
El historial completo sigue en el estado; el filtro solo afecta al prompt del LLM.

Artículo: ../Teoria_Tipos_Memoria_LangGraph.md
"""
from dotenv import find_dotenv, load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, START, StateGraph

load_dotenv(find_dotenv())

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
workflow = StateGraph(MessagesState)


def filter_important_messages(messages: list[BaseMessage]) -> list[BaseMessage]:
    """Versión del artículo: filter_important_messages (solo lectura para el LLM)."""
    if len(messages) <= 8:
        return list(messages)

    important_messages: list[BaseMessage] = []
    regular_messages: list[BaseMessage] = []

    for msg in messages:
        content = getattr(msg, "content", "") or ""
        is_important = (
            isinstance(msg, SystemMessage)
            or "importante" in content.lower()
            or "recuerda" in content.lower()
            or "preferencia" in content.lower()
            or len(content) > 200
        )
        if is_important:
            important_messages.append(msg)
        else:
            regular_messages.append(msg)

    return important_messages + regular_messages[-4:]


def chatbot_node(state: MessagesState):
    all_messages = list(state["messages"])
    messages_for_llm = filter_important_messages(all_messages)
    system = SystemMessage(
        content="Eres un asistente útil. Prioriza mensajes marcados como importantes o recuerda."
    )
    response = llm.invoke([system] + messages_for_llm)
    return {"messages": [response]}


workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)
app = workflow.compile(checkpointer=MemorySaver())


def chat(text: str, thread_id: str = "sesion_filtro") -> str:
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"messages": [HumanMessage(content=text)]}, config)
    return result["messages"][-1].content


if __name__ == "__main__":
    print("=== 2. Memoria de filtrado inteligente ===")
    print("Prueba: 'Recuerda que soy alérgico al maná' y luego muchos mensajes cortos.\n")
    tid = "sesion_filtro"
    while True:
        try:
            user = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user or user.lower() in {"salir", "exit", "quit"}:
            print("Hasta luego.")
            break
        print("Asistente:", chat(user, tid), "\n")

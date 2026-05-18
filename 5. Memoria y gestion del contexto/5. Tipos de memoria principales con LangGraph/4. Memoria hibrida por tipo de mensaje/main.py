"""
Estrategia 4: Memoria híbrida por tipo de mensaje.

- Todos los SystemMessage
- Últimos 4 HumanMessage
- Últimas 2 AIMessage
Reordenados en orden cronológico (como en el artículo).

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


def hybrid_memory_management(messages: list[BaseMessage]) -> list[BaseMessage]:
    """Versión del artículo: hybrid_memory_management."""
    if len(messages) <= 6:
        return list(messages)

    system_messages: list[BaseMessage] = []
    human_messages: list[BaseMessage] = []
    ai_messages: list[BaseMessage] = []

    for msg in messages:
        if isinstance(msg, SystemMessage):
            system_messages.append(msg)
        elif isinstance(msg, HumanMessage):
            human_messages.append(msg)
        elif isinstance(msg, AIMessage):
            ai_messages.append(msg)

    filtered: list[BaseMessage] = []
    filtered.extend(system_messages)
    filtered.extend(human_messages[-4:])
    filtered.extend(ai_messages[-2:])
    filtered.sort(key=lambda x: messages.index(x))
    return filtered


def chatbot_node(state: MessagesState):
    all_messages = list(state["messages"])
    messages_for_llm = hybrid_memory_management(all_messages)
    system = SystemMessage(content="Eres un asistente útil en un chat de juego.")
    response = llm.invoke([system] + messages_for_llm)
    return {"messages": [response]}


workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)
app = workflow.compile(checkpointer=MemorySaver())


def chat(text: str, thread_id: str = "sesion_hibrida") -> str:
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"messages": [HumanMessage(content=text)]}, config)
    return result["messages"][-1].content


if __name__ == "__main__":
    print("=== 4. Memoria híbrida por tipo de mensaje ===")
    print("System: todos | Human: últimos 4 | AI: últimas 2 respuestas.\n")
    tid = "sesion_hibrida"
    while True:
        try:
            user = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user or user.lower() in {"salir", "exit", "quit"}:
            print("Hasta luego.")
            break
        print("Asistente:", chat(user, tid), "\n")

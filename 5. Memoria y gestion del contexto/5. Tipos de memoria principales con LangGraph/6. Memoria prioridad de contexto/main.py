"""
Estrategia 6: Memoria con prioridad de contexto.

Puntúa mensajes por keywords extraídos de los últimos 3 turnos + bonus de recencia.
Se quedan los 8 mensajes con mayor puntuación (orden cronológico al final).

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


def extract_keywords(text: str) -> list[str]:
    words = text.lower().split()
    stop_words = {"el", "la", "de", "que", "y", "en", "un", "es", "se", "no", "te", "lo"}
    keywords = [w for w in words if len(w) > 3 and w not in stop_words]
    return list(set(keywords))[:10]


def calculate_relevance(text: str, keywords: list[str]) -> float:
    text_lower = text.lower()
    matches = sum(1 for keyword in keywords if keyword in text_lower)
    return matches / max(len(keywords), 1)


def priority_context_memory(messages: list[BaseMessage]) -> list[BaseMessage]:
    if len(messages) <= 8:
        return list(messages)

    recent_content = " ".join(getattr(m, "content", "") or "" for m in messages[-3:])
    current_keywords = extract_keywords(recent_content)

    scored_messages: list[tuple[float, BaseMessage]] = []
    for i, msg in enumerate(messages):
        content = getattr(msg, "content", "") or ""
        relevance_score = calculate_relevance(content, current_keywords)
        recency_bonus = max(0, len(messages) - i) * 0.1
        scored_messages.append((relevance_score + recency_bonus, msg))

    scored_messages.sort(key=lambda x: x[0], reverse=True)
    selected = [msg for _, msg in scored_messages[:8]]
    selected.sort(key=lambda x: messages.index(x))
    return selected


def chatbot_node(state: MessagesState):
    all_messages = list(state["messages"])
    messages_for_llm = priority_context_memory(all_messages)
    system = SystemMessage(
        content="Eres un asistente útil. Prioriza el tema de los mensajes recientes."
    )
    response = llm.invoke([system] + messages_for_llm)
    return {"messages": [response]}


workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)
app = workflow.compile(checkpointer=MemorySaver())


def chat(text: str, thread_id: str = "sesion_prioridad") -> str:
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"messages": [HumanMessage(content=text)]}, config)
    return result["messages"][-1].content


if __name__ == "__main__":
    print("=== 6. Memoria con prioridad de contexto ===")
    print("Cambia de tema y mira qué mensajes antiguos siguen entrando al LLM.\n")
    tid = "sesion_prioridad"
    while True:
        try:
            user = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user or user.lower() in {"salir", "exit", "quit"}:
            print("Hasta luego.")
            break
        print("Asistente:", chat(user, tid), "\n")

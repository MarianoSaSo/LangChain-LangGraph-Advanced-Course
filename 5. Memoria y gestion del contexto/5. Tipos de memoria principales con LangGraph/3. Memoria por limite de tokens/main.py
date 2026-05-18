"""
Estrategia 3: Memoria por límite de tokens (estimación simple).

estimate_tokens ≈ len(texto) // 4. Si supera MAX_TOKENS, se quedan mensajes recientes
hasta caber en el presupuesto (respetando un SystemMessage inicial si existe).

Artículo: ../Teoria_Tipos_Memoria_LangGraph.md
"""
from dotenv import find_dotenv, load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, START, StateGraph

load_dotenv(find_dotenv())

MAX_TOKENS = 2000  # Mismo valor por defecto que en el artículo (check_token_limit)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
workflow = StateGraph(MessagesState)


def estimate_tokens(text: str) -> int:
    """Estimación del artículo: ~4 caracteres por token."""
    return len(text) // 4


def manage_memory_by_tokens(messages: list[BaseMessage], max_tokens: int = MAX_TOKENS) -> list[BaseMessage]:
    """Versión del artículo adaptada: devuelve la lista recortada para el LLM."""
    total_tokens = sum(estimate_tokens(getattr(m, "content", "") or "") for m in messages)
    if total_tokens <= max_tokens:
        return list(messages)

    if messages and isinstance(messages[0], SystemMessage):
        system_msg = messages[0]
        other_messages = messages[1:]
        current_tokens = estimate_tokens(system_msg.content)
    else:
        system_msg = None
        other_messages = messages
        current_tokens = 0

    selected_messages: list[BaseMessage] = []
    for msg in reversed(other_messages):
        msg_tokens = estimate_tokens(getattr(msg, "content", "") or "")
        if current_tokens + msg_tokens <= max_tokens:
            selected_messages.insert(0, msg)
            current_tokens += msg_tokens
        else:
            break

    final: list[BaseMessage] = []
    if system_msg:
        final.append(system_msg)
    final.extend(selected_messages)
    return final


def chatbot_node(state: MessagesState):
    all_messages = list(state["messages"])
    messages_for_llm = manage_memory_by_tokens(all_messages)
    system = SystemMessage(content="Eres un asistente útil. Responde con el contexto disponible.")
    response = llm.invoke([system] + messages_for_llm)
    return {"messages": [response]}


workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)
app = workflow.compile(checkpointer=MemorySaver())


def chat(text: str, thread_id: str = "sesion_tokens") -> str:
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"messages": [HumanMessage(content=text)]}, config)
    return result["messages"][-1].content


if __name__ == "__main__":
    print("=== 3. Memoria por límite de tokens ===")
    print(f"Presupuesto estimado: {MAX_TOKENS} tokens (~{MAX_TOKENS * 4} caracteres).\n")
    tid = "sesion_tokens"
    while True:
        try:
            user = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user or user.lower() in {"salir", "exit", "quit"}:
            print("Hasta luego.")
            break
        print("Asistente:", chat(user, tid), "\n")

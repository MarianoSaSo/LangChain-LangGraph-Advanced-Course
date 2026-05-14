"""
Nodos del grafo LangGraph.

Este mini proyecto usa un solo nodo (el tendero). Más adelante podríais
añadir otro nodo (por ejemplo "tasador de loot" o "rumores del pueblo")
y aristas condicionales sin cambiar la organización de carpetas.
"""
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState

from config import get_llm_temperature, get_openai_model
from prompts.tendero_system import SYSTEM_PROMPT_TENDERO

# Una sola instancia de LLM por proceso (suficiente para este mini proyecto).
_llm: ChatOpenAI | None = None


def _get_llm() -> ChatOpenAI:
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(model=get_openai_model(), temperature=get_llm_temperature())
    return _llm


def tendero_node(state: MessagesState):
    """
    Lee el historial en state['messages'], añade el system prompt del NPC
    y devuelve solo la nueva respuesta del modelo (LangGraph concatena al historial).
    """
    llm = _get_llm()
    messages_for_llm = [SystemMessage(content=SYSTEM_PROMPT_TENDERO)] + list(state["messages"])
    response = llm.invoke(messages_for_llm)
    return {"messages": [response]}

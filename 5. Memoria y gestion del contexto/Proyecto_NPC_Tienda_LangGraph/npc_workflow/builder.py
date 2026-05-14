"""
Construcción y compilación del grafo.

Aquí solo se ensamblan: esquema de estado, nodos, aristas y checkpointer.
Así el resto del código no mezcla "topología del grafo" con la interfaz de usuario.
"""
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph

from npc_workflow.nodes import tendero_node


def build_compiled_npc_graph():
    workflow = StateGraph(MessagesState)
    workflow.add_node("tendero", tendero_node)
    workflow.add_edge(START, "tendero")
    workflow.add_edge("tendero", END)
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

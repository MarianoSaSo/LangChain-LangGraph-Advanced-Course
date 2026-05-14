"""
Capa de servicio: orquesta invocaciones al grafo compilado.

En aplicaciones reales, la UI (Streamlit, API FastAPI, etc.) llama a esta capa
y no importa `langgraph` directamente. Eso facilita tests y cambios de motor.
"""
from langchain_core.messages import HumanMessage


class NpcChatService:
    def __init__(self, compiled_graph):
        self._app = compiled_graph

    def reply(self, user_text: str, thread_id: str) -> str:
        config = {"configurable": {"thread_id": thread_id}}
        result = self._app.invoke({"messages": [HumanMessage(content=user_text)]}, config)
        return result["messages"][-1].content

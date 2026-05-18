"""
=============================================================================
LECCIÓN: Memoria de resumen (Summarization Memory) con LangGraph
=============================================================================

IDEA EN UNA FRASE:
  Guardamos TODA la conversación en el estado, pero al modelo solo le
  mandamos un RESUMEN de lo antiguo + los ÚLTIMOS mensajes cuando el chat
  es largo.

Guía extendida (diagramas y pruebas): Explicacion_Memoria_Resumen.md
Artículo general: ../Teoria_Tipos_Memoria_LangGraph.md
"""
from typing import Annotated, TypedDict

from dotenv import find_dotenv, load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

# Carga OPENAI_API_KEY desde el .env de la raíz del curso (find_dotenv sube carpetas).
load_dotenv(find_dotenv())

# ---------------------------------------------------------------------------
# PARÁMETROS (ajústalos en clase para ver el efecto)
# ---------------------------------------------------------------------------
# Cuando el historial tiene ESTE número de mensajes o más, activamos el resumen.
UMBRAL_RESUMIR = 10

# Cuántos mensajes recientes mandamos ENTEROS (sin resumir) junto al resumen.
# Ejemplo: con 10 mensajes totales, resumimos los 6 primeros y dejamos los 4 últimos.
MENSAJES_RECIENTES = 4

# Modelo compartido: lo usamos para (1) crear el resumen y (2) responder al usuario.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ---------------------------------------------------------------------------
# ESTADO DEL GRAFO (más campos que MessagesState simple)
# ---------------------------------------------------------------------------
class SummaryState(TypedDict, total=False):
    """
    TypedDict = “forma” del diccionario de estado que comparten los nodos.

    Campos:
      messages:
        Lista de HumanMessage / AIMessage / etc.
        Annotated[..., add_messages] le dice a LangGraph:
        “cuando un nodo devuelve {"messages": [nuevo]}, AÑÁDELO al final,
        no reemplaces toda la lista”.
        Por eso el historial COMPLETO sigue creciendo en MemorySaver.

      conversation_summary:
        Texto con el último resumen generado (como un “apunte” de lo antiguo).
        No sustituye a messages; es un campo aparte que actualizamos nosotros.

      message_count:
        Contador opcional (viene del artículo del curso). Aquí guardamos
        cuántos mensajes llevamos; sirve para depurar o ampliar la lógica.
    """
    messages: Annotated[list[BaseMessage], add_messages]
    conversation_summary: str
    message_count: int


def build_messages_for_llm(
    messages: list[BaseMessage],
    current_summary: str,
) -> tuple[list[BaseMessage], str]:
    """
    Prepara QUÉ leerá el modelo en ESTE turno (no modifica el historial guardado).

    Devuelve:
      - lista de mensajes para el prompt (resumen + recientes, o todo el historial)
      - texto del resumen actualizado (igual al anterior si aún no toca resumir)

    PASO A PASO cuando len(messages) >= UMBRAL_RESUMIR:
      1) recent_messages  = los 4 últimos (conversación “fresca”).
      2) messages_to_summarize = todo lo anterior (lo “viejo”).
      3) Llamada extra al LLM solo para condensar lo viejo (+ resumen previo).
      4) Metemos ese texto en un SystemMessage y lo concatenamos con los 4 recientes.
    """
    # ----- Caso A: conversación corta → el modelo ve todo el historial -----
    if len(messages) < UMBRAL_RESUMIR:
        return list(messages), current_summary

    # ----- Caso B: conversación larga → resumir lo antiguo, conservar el final -----
    recent_messages = messages[-MENSAJES_RECIENTES:]
    messages_to_summarize = messages[:-MENSAJES_RECIENTES]

    # Texto plano de los mensajes viejos (type = "human" | "ai" | "system" ...)
    lines = [f"{m.type}: {m.content}" for m in messages_to_summarize]

    # PRIMERA llamada al LLM en este turno: solo para generar el resumen.
    # No es la respuesta que verá el usuario en la terminal.
    summary_prompt = f"""Eres un asistente que resume conversaciones.
Resumen anterior: {current_summary or "(ninguno)"}

Mensajes a resumir:
{chr(10).join(lines)}

Escribe un resumen breve en español con los puntos clave (máximo 8 líneas).
Incluye nombres, preferencias y datos importantes que aparezcan.
Solo el resumen, sin preámbulos."""

    new_summary = llm.invoke([HumanMessage(content=summary_prompt)]).content

    # Este SystemMessage es “memoria comprimida” que verá el modelo en la 2ª llamada.
    summary_message = SystemMessage(
        content=f"Resumen de conversación previa: {new_summary}"
    )

    # Lo que el chatbot enviará al LLM: resumen + ventana de mensajes recientes.
    messages_for_llm = [summary_message] + recent_messages
    return messages_for_llm, new_summary


# ---------------------------------------------------------------------------
# GRAFO (un solo nodo, como en lecciones anteriores)
# ---------------------------------------------------------------------------
workflow = StateGraph(SummaryState)


def chatbot_node(state: SummaryState):
    """
    Nodo que se ejecuta en cada turno del usuario.

    Entrada (state):
      - messages: historial completo recuperado del checkpointer.
      - conversation_summary: resumen guardado en el turno anterior (si existe).

    Salida (return):
      - messages: [nueva respuesta del asistente] → se AÑADE al historial.
      - conversation_summary: actualizado si hemos vuelto a resumir.
      - message_count: tamaño aproximado del historial tras este turno.
    """
    # Copia de la lista completa (puede tener decenas de mensajes guardados).
    all_messages = list(state["messages"])
    current_summary = state.get("conversation_summary", "")

    # -------------------------------------------------------------------------
    # SINTAXIS:  a, b = funcion(...)
    # -------------------------------------------------------------------------
    # build_messages_for_llm DEVUELVE DOS COSAS a la vez (una tupla de 2 elementos):
    #   1) messages_for_llm  → lista de mensajes que le pasaremos al LLM en este turno
    #   2) updated_summary   → texto del resumen (nuevo o igual que current_summary)
    #
    # Es equivalente a escribir:
    #   resultado = build_messages_for_llm(all_messages, current_summary)
    #   messages_for_llm = resultado[0]
    #   updated_summary = resultado[1]
    #
    # NO borra all_messages del estado: solo calcula qué subset usar para el prompt.
    messages_for_llm, updated_summary = build_messages_for_llm(
        all_messages, current_summary
    )

    # Instrucción fija del asistente + contexto ya recortado/resumido.
    system = SystemMessage(
        content=(
            "Eres un asistente útil. "
            "Si hay un resumen de conversación previa, úsalo para contestar. "
            "Si algo no está en el resumen ni en los mensajes recientes, dilo con honestidad."
        )
    )

    # SEGUNDA llamada al LLM en este turno (cuando hubo resumen): la respuesta al usuario.
    response = llm.invoke([system] + messages_for_llm)

    # -------------------------------------------------------------------------
    # SINTAXIS:  out: SummaryState = { ... }
    # -------------------------------------------------------------------------
    # - "out" NO es una palabra reservada de Python. Es solo un nombre de variable
    #   que elegimos (= "salida", "output"). Podríamos llamarla actualizacion o datos.
    #
    # - "out: SummaryState" es una ANOTACIÓN DE TIPO (type hint):
    #     le dice al lector (y al IDE) "out será un diccionario con forma SummaryState".
    #   NO crea el diccionario por sí sola; lo que crea el dict es lo de después del "=".
    #
    # - Un nodo de LangGraph debe DEVOLVER un dict con SOLO los campos del estado que
    #   quieres actualizar en este paso. LangGraph los fusiona con el estado anterior.
    #
    # Qué va dentro de "out":
    #   "messages": [response]  → solo el mensaje NUEVO del asistente (no toda la lista).
    #                             add_messages lo AÑADE al final del historial guardado.
    #   "message_count": ...   → actualizamos el contador auxiliar del estado.
    out: SummaryState = {
        "messages": [response],
        "message_count": len(all_messages) + 1,
    }

    # Solo guardamos conversation_summary en el estado si cambió (hubo resumen nuevo).
    # out["clave"] = valor  → añade o modifica una entrada en el diccionario out.
    if updated_summary != current_summary:
        out["conversation_summary"] = updated_summary

    # return out  → LangGraph recibe este dict y actualiza el estado de la conversación.
    return out


workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

# MemorySaver = memoria en RAM por thread_id (igual que lección 3).
# Guarda snapshots del estado (messages + conversation_summary + ...).
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def chat(text: str, thread_id: str = "sesion_resumen") -> str:
    """
    Envía un mensaje del usuario al grafo compilado.

    thread_id:
      Identificador de la conversación. Mismo id → misma sesión en memoria.
      Cambia el id si quieres empezar un chat vacío sin borrar el programa.
    """
    config = {"configurable": {"thread_id": thread_id}}

    # Solo inyectamos el mensaje humano nuevo; LangGraph fusiona con el estado previo.
    result = app.invoke({"messages": [HumanMessage(content=text)]}, config)

    # La última entrada de messages es la respuesta del asistente de este turno.
    return result["messages"][-1].content


if __name__ == "__main__":
    print("=== 1. Memoria de resumen ===")
    print(f"- Historial completo: siempre guardado en MemorySaver.")
    print(f"- Al LLM: si hay >= {UMBRAL_RESUMIR} mensajes → resumen + últimos {MENSAJES_RECIENTES}.")
    print("- Cada turno 'largo' hace 2 llamadas al modelo (resumir + responder).")
    print("Escribe 'salir' para terminar.\n")

    # Un solo thread en esta demo; en una app real sería un id por usuario.
    thread_id = "sesion_resumen"

    while True:
        try:
            user_input = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego.")
            break

        if not user_input:
            continue
        if user_input.lower() in {"salir", "exit", "quit"}:
            print("Hasta luego.")
            break

        respuesta = chat(user_input, thread_id)
        print(f"Asistente: {respuesta}\n")

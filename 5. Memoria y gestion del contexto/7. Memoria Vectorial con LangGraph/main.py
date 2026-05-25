"""
=============================================================================
LECCION 7: Memoria vectorial con LangGraph (caso practico en terminal)
=============================================================================

Dos memorias a la vez:
  1) MemorySaver (RAM)  -> historial de ESTA conversacion (volatil al cerrar el programa).
  2) ChromaDB (disco)   -> datos personales del usuario (nombre, gustos...) para TODAS las sesiones.

Teoria: Teoria_Memoria_Vectorial_LangGraph.md

Chroma se importa desde langchain_community (mismo stack 0.3.x que el resto del curso).
No instales langchain-chroma: rompe las versiones de langchain-core del venv.
"""
from __future__ import annotations

import uuid
from pathlib import Path

import chromadb
from dotenv import find_dotenv, load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, START, StateGraph

# ---------------------------------------------------------------------------
# Rutas: carpeta de ESTE script (funciona en cualquier PC, no rutas fijas)
# ---------------------------------------------------------------------------
load_dotenv(find_dotenv())  # Carga OPENAI_API_KEY desde el .env de la raiz del curso

BASE_DIR = Path(__file__).resolve().parent
# Carpeta donde Chroma guarda la base de datos en disco (se crea sola al ejecutar)
CHROMADB_PATH = str(BASE_DIR / "chroma_db")

# ---------------------------------------------------------------------------
# IMPORTS explicados (para estudiantes)
# ---------------------------------------------------------------------------
# - MessagesState: estado del grafo con lista "messages" (historial de chat).
# - MemorySaver: guarda checkpoints del grafo en RAM por thread_id.
# - Chroma (langchain_community): envoltorio LangChain sobre ChromaDB (igual que en el modulo RAG).
# - chromadb.PersistentClient: cliente "bajo nivel" de Chroma para add/query/get sin LangChain.
# - OpenAIEmbeddings: convierte texto en vectores numericos para buscar por significado.
# - uuid: genera IDs unicos para cada documento guardado en la coleccion.

# ---------------------------------------------------------------------------
# 1) Modelo de lenguaje (el "cerebro" que redacta respuestas)
# ---------------------------------------------------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,  # 0 = respuestas mas predecibles (menos creatividad aleatoria)
)

# ---------------------------------------------------------------------------
# 2) Base de datos vectorial (memoria GENERAL del usuario, persiste en disco)
# ---------------------------------------------------------------------------
# vectorstore (LangChain): crea o abre la coleccion y configura embeddings.
# Es la forma "alta" de trabajar con Chroma. Si la carpeta no existe, la crea.
vectorstore = Chroma(
    collection_name="memoria_chat",  # "Apartado" dentro de Chroma (como una BD dentro del servidor)
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"),
    persist_directory=CHROMADB_PATH,
)

# client (ChromaDB directo): conexion al mismo archivo en disco que vectorstore.
# Sirve para operaciones simples que en la leccion hacemos a mano (add, query, get).
client = chromadb.PersistentClient(path=CHROMADB_PATH)

# collection: la "tabla" / estanteria concreta donde guardamos textos del usuario.
# get_or_create_collection evita error la primera vez que ejecutas el programa.
collection = client.get_or_create_collection(name="memoria_chat")


def guardar_memoria(texto: str) -> None:
    """
    Guarda un texto en la memoria vectorial (disco).

    Cada guardado:
      - Convierte el texto a vector (embeddings) automaticamente al buscar/guardar via Chroma.
      - Necesita un id unico por documento; usamos uuid4 para no pisar registros viejos.
    """
    try:
        collection.add(
            documents=[texto],  # Lista: Chroma admite varios documentos a la vez
            ids=[str(uuid.uuid4())],  # ID obligatorio; si no pones, Chroma inventa uno
        )
        print(f"[+] Guardado en memoria: {texto}")
    except Exception as e:
        print(f"Error guardando en memoria: {texto} -> {e}")


def buscar_memoria(consulta: str, k: int = 3) -> list[str]:
    """
    Busca en Chroma los k textos mas parecidos (por significado) a la consulta.

    Ejemplo: si guardaste "Le gusta: me encanta Alemania" y preguntas "que destinos me recomiendas",
    la busqueda vectorial puede recuperar ese fragmento aunque no repitas las mismas palabras.

    Nota didactica: aqui usamos collection.query (API cruda). En proyectos grandes
    usarias un Retriever de LangChain (MMR, MultiQuery, etc.) como en el modulo RAG.
    """
    try:
        results = collection.query(
            query_texts=[consulta],  # Chroma embede esta frase y compara con lo guardado
            n_results=k,
        )
        # results["documents"] es lista de listas: [ [doc1, doc2, ...] ]
        if results.get("documents") and results["documents"][0]:
            return results["documents"][0]
        return []
    except Exception:
        return []


def _extraer_texto_ultimo_mensaje(messages: list) -> str:
    """Devuelve el contenido del ultimo mensaje humano, o cadena vacia si no hay mensajes."""
    if not messages:
        return ""
    ultimo = messages[-1]
    return getattr(ultimo, "content", str(ultimo))


def chatbot_node(state: MessagesState) -> dict:
    """
    Nodo principal del grafo. Se ejecuta UNA vez por cada mensaje del usuario.

    Flujo:
      1) Leer ultimo mensaje del usuario.
      2) Buscar en Chroma recuerdos relevantes (memoria general).
      3) Montar SystemMessage con esos recuerdos + llamar al LLM con historial (MemorySaver).
      4) Si el mensaje trae datos personales (heuristicas), guardarlos en Chroma.
      5) Devolver la respuesta del modelo para que LangGraph la anada al estado.
    """
    messages = state["messages"]
    ultimo_mensaje = _extraer_texto_ultimo_mensaje(messages)

    # --- Paso 1: recuperar memoria historica vectorial ---
    memorias = buscar_memoria(ultimo_mensaje)

    # --- Paso 2: prompt de sistema dinamico (lo que "recuerda" de otros chats) ---
    system_content = "Eres un asistente que recuerda informacion importante."
    if memorias:
        system_content += "\n\nInformacion que recuerdas:"
        for memoria in memorias:
            system_content += f"\n- {memoria}"

    # --- Paso 3: el LLM ve [instrucciones] + [historial de ESTA sesion en MemorySaver] ---
    messages_con_sistema = [SystemMessage(content=system_content)] + list(messages)
    response = llm.invoke(messages_con_sistema)

    # --- Paso 4: guardar datos personales nuevos (metodo rudimentario por palabras clave) ---
    # En produccion usarias otro LLM que decida QUE guardar; aqui es didactico y simple.
    mensaje_lower = ultimo_mensaje.lower()
    if "me llamo" in mensaje_lower:
        guardar_memoria(f"El usuario se llama: {ultimo_mensaje}")
    elif any(
        frase in mensaje_lower
        for frase in [
            "trabajo en",
            "trabajo como",
            "soy programador",
            "soy doctor",
            "soy estudiante",
        ]
    ):
        guardar_memoria(f"Trabajo del usuario: {ultimo_mensaje}")
    elif "me gusta" in mensaje_lower or "me encanta" in mensaje_lower:
        guardar_memoria(f"Le gusta: {ultimo_mensaje}")
    elif "vivo en" in mensaje_lower or "soy de" in mensaje_lower:
        guardar_memoria(f"Ubicacion: {ultimo_mensaje}")

    # LangGraph fusiona esta lista nueva con el historial existente (reducer de messages)
    return {"messages": [response]}


# ---------------------------------------------------------------------------
# 3) Construccion del grafo LangGraph
# ---------------------------------------------------------------------------
workflow = StateGraph(MessagesState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)  # Tras responder, termina esta "vuelta" del grafo

# MemorySaver = memoria VOLATIL de la conversacion (se pierde al cerrar el proceso)
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def chat(message: str, thread_id: str = "sesion_terminal") -> str:
    """
    Envia un mensaje al grafo y devuelve solo el texto de la ultima respuesta.

    thread_id identifica la conversacion:
      - Mismo thread_id  -> mismo historial en MemorySaver.
      - Distinto thread_id -> chat nuevo en RAM, pero misma memoria vectorial en Chroma.
    """
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke(
        {"messages": [HumanMessage(content=message)]},
        config,
    )
    return result["messages"][-1].content


def mostrar_memorias() -> None:
    """Lista todo lo guardado en Chroma (memoria general), sin importar el thread_id."""
    try:
        all_memories = collection.get()
        documentos = all_memories.get("documents") or []
        if documentos:
            print("[+] Memorias guardadas (ChromaDB / memoria general):")
            for i, memoria in enumerate(documentos, 1):
                print(f"  {i}. {memoria}")
        else:
            print("[-] No hay memorias guardadas aun")
    except Exception as e:
        print(f"Error obteniendo memorias: {e}")


if __name__ == "__main__":
    print(
        "Chat en terminal\n"
        "  - Escribe tu mensaje y pulsa Enter\n"
        "  - 'memorias' -> ver lo guardado en Chroma (disco)\n"
        "  - 'salir'    -> cerrar\n"
    )
    # Cambia este valor para simular otro chat en RAM (ej: sesion_terminal_2)
    session_id = "sesion_terminal"

    while True:
        try:
            user_input = input("Tu: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"salir", "exit", "quit"}:
            print("Hasta luego!")
            break
        if user_input.lower() == "memorias":
            mostrar_memorias()
            continue

        respuesta = chat(user_input, session_id)
        print("Asistente:", respuesta)
        print()

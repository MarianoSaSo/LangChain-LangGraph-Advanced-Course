"""
Punto de entrada del mini proyecto (chat en terminal).

Ejecutar desde esta carpeta del proyecto, con el venv del curso activado:

    cd "...\\Proyecto_NPC_Tienda_LangGraph"
    ..\\..\\venv\\Scripts\\Activate.ps1
    python main.py
"""
import os
import sys
from pathlib import Path

# Asegurar imports del proyecto (mismo patrón que otros proyectos del curso)
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# config se importa al cargar el resto; fuerza carga temprana de .env
import config  # noqa: F401

from npc_workflow.builder import build_compiled_npc_graph
from services.npc_chat_service import NpcChatService


def _exit_if_no_openai_key() -> None:
    if os.getenv("OPENAI_API_KEY"):
        return
    print(
        "ERROR: no está definida OPENAI_API_KEY.\n"
        f"- Crea el archivo .env en la raíz del curso (por ejemplo):\n  {config.CURSO_ROOT / '.env'}\n"
        f"- O en la carpeta del proyecto:\n  {config.PROJECT_ROOT / '.env'}\n"
        "Copia de plantilla: .env.example en la raíz del repositorio.\n"
    )
    sys.exit(1)


def main() -> None:
    _exit_if_no_openai_key()
    graph = build_compiled_npc_graph()
    npc = NpcChatService(graph)

    print("=== Tienda del pueblo (NPC + LangGraph + MemorySaver) ===")
    print("Escribe 'salir' para terminar.\n")

    # En una app web, thread_id sería por usuario o por partida guardada en BD.
    thread_id = "partida_practica_01"

    while True:
        try:
            user_input = input("Jugador: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n¡Hasta la próxima!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"salir", "exit", "quit"}:
            print("Tendero: ¡Que los dioses guíen tu espada, forastero!")
            break

        reply = npc.reply(user_input, thread_id=thread_id)
        print(f"Tendero: {reply}\n")


if __name__ == "__main__":
    main()

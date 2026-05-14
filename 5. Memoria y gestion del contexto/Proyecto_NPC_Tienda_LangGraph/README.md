# Mini proyecto: NPC tendero (LangGraph + MemorySaver)

Chat en terminal con un **NPC de tienda de RPG**. Sirve para practicar el mismo patrón que en la lección 3 del tema 5 (`MessagesState`, `MemorySaver`, `thread_id`), pero con una **estructura de carpetas parecida a un proyecto pequeño real**.

## Idea del juego (didáctica)

Eres el jugador; el modelo interpreta al **tendero del pueblo**. La memoria conversacional permite que recuerde cosas como tu **nombre**, **qué buscabas** o **acuerdos de precio** inventados en la misma sesión (mientras el proceso siga en marcha y uses el mismo `thread_id`).

## Estructura de carpetas

```text
Proyecto_NPC_Tienda_LangGraph/
├── main.py                 # Arranque: bucle de terminal
├── config.py               # Variables de entorno y ajustes
├── prompts/                # Textos del sistema (personaje)
│   ├── __init__.py
│   └── tendero_system.py
├── npc_workflow/           # Grafo LangGraph (nodos + compilación)
│   ├── __init__.py
│   ├── builder.py          # StateGraph + MemorySaver + compile
│   └── nodes.py            # Lógica del nodo "tendero"
└── services/               # Capa que usaría una API o una UI
    ├── __init__.py
    └── npc_chat_service.py # reply(mensaje, thread_id)
```

**Por qué así:** separar *prompts*, *workflow* y *servicios* evita un único archivo gigante y es el mismo criterio que en proyectos mayores del curso (`services/`, `prompts/`, etc.), aunque aquí sea mini.

## Requisitos

Usa el **mismo `venv` y `requirements.txt`** de la raíz del curso. Necesitas `OPENAI_API_KEY` en el `.env` de la raíz del repositorio (o un `.env` dentro de esta carpeta del proyecto).

Opcional en el `.env` de la raíz del curso:

```env
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3
```

## Cómo ejecutarlo

Desde PowerShell:

```powershell
cd "c:\Users\maria\Desktop\LangChain & LangGraph\5. Memoria y gestion del contexto\Proyecto_NPC_Tienda_LangGraph"
..\..\venv\Scripts\Activate.ps1
python main.py
```

## Prácticas sugeridas

1. Cambia el tono del tendero editando solo `prompts/tendero_system.py`.
2. Duplica el `thread_id` en dos terminales distintas con valores distintos y comprueba que **no** comparten historial.
3. (Avanzado) Añade un segundo nodo en `npc_workflow/` (por ejemplo “rumores”) y una arista condicional en `builder.py`.

## Objetivo de aprendizaje

Relacionar **organización de código** con **conceptos de LangGraph**: el grafo compilado vive en el “motor” (`npc_workflow`), la **interfaz** solo habla con `NpcChatService`, y los **textos** viven en `prompts/`.

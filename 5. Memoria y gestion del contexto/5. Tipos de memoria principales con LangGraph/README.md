# Tipos de memoria principales con LangGraph

## Lectura obligatoria

- **[Teoria_Tipos_Memoria_LangGraph.md](./Teoria_Tipos_Memoria_LangGraph.md)** — artículo completo del curso.

## Ejemplos ejecutables

Cada carpeta tiene un `main.py` independiente (mismo patrón: `StateGraph` + `MemorySaver` + chat en terminal).

| Carpeta | Comando (desde la carpeta del ejemplo) |
|---------|----------------------------------------|
| `1. Memoria de resumen` | `python main.py` |
| `2. Memoria de filtrado inteligente` | `python main.py` |
| `3. Memoria por limite de tokens` | `python main.py` |
| `4. Memoria hibrida por tipo de mensaje` | `python main.py` |
| `5. Memoria ventana deslizante adaptativa` | `python main.py` |
| `6. Memoria prioridad de contexto` | `python main.py` |

Activa el venv del curso desde cualquier ejemplo:

```powershell
cd "c:\Users\maria\Desktop\LangChain & LangGraph\5. Memoria y gestion del contexto\5. Tipos de memoria principales con LangGraph\1. Memoria de resumen"
..\..\..\venv\Scripts\Activate.ps1
python main.py
```

Desde cualquier subcarpeta `1.` … `6.`: sube **tres** niveles (`..\..\..`) hasta la raíz del curso donde está `venv`.

Requisito: `OPENAI_API_KEY` en el `.env` de la raíz del repositorio.

## Relación con otras lecciones del tema 5

- **Lección 3:** memoria completa al LLM (`MemorySaver`).
- **Lección 4:** ventana deslizante fija (`trim_messages`).
- **Esta unidad:** panorama de estrategias + código de referencia por técnica.

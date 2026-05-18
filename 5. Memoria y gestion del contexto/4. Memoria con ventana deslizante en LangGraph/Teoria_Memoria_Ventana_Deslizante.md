# Memoria con ventana deslizante en LangGraph

Continuación de la lección anterior (**memoria completa** con `MessagesState` + `MemorySaver`). Aquí aprendes una estrategia muy usada en producción: **no mandar todo el historial al LLM**, sino solo los **últimos N mensajes**.

---

## 1. ¿Por qué no basta con “guardar todo”?

En la lección 3 el checkpointer guardaba **cada mensaje** y el nodo enviaba **todo** `state["messages"]` al modelo.

Eso funciona bien al principio, pero en conversaciones largas aparecen problemas:

| Problema | Qué pasa |
|----------|----------|
| **Ventana de contexto** | El modelo tiene un límite de tokens; un historial enorme puede dar error o respuestas peores. |
| **Coste** | La facturación depende de los tokens que envías en cada llamada. |
| **Abuso / ruido** | Un usuario podría enviar miles de mensajes y inflar cada petición. |

Por eso existen **varias estrategias de memoria** (no solo “todo o nada”):

- **Ventana deslizante** (esta lección): últimos *N* mensajes.
- **Memoria con resumen**: un texto corto que condensa lo antiguo.
- **Límite por tokens**: recortar por tokens reales, no por número de mensajes.
- **Memoria vectorial**: recuperar solo fragmentos relevantes (RAG de la conversación).

En el curso veréis más adelante otras; aquí nos centramos en la **ventana deslizante**.

---

## 2. Idea clave de esta lección (dos capas)

Muchos alumnos se confunden aquí. Hay **dos sitios** donde vive la memoria:

```
┌─────────────────────────────────────────────────────────────┐
│  MemorySaver (checkpointer)                                 │
│  → Guarda el historial COMPLETO por thread_id               │
│  → Podrías auditar o exportar todo (si lo necesitas)        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Nodo chatbot + trim_messages                               │
│  → Solo al LLM le llegan los últimos N mensajes (ventana)   │
│  → El modelo “olvida” lo que quedó fuera de la ventana      │
└─────────────────────────────────────────────────────────────┘
```

**No borramos** mensajes viejos del estado en disco/RAM del grafo: **recortamos solo en el momento de llamar al LLM**.

Eso explica la demo del vídeo: tras muchas preguntas sobre Alemania, el modelo **sigue** respondiendo sobre la bandera alemana (está en la ventana), pero si preguntas **“¿cómo me llamo?”** y tu nombre fue al principio, puede responder *“no tengo acceso a tu nombre”* porque ese mensaje **ya no entra** en los 4 últimos.

---

## 3. `trim_messages` (LangChain Core)

Función importada desde:

```python
from langchain_core.messages import trim_messages
```

No es de LangGraph: es una utilidad de **LangChain Core** para recortar listas de mensajes.

Por defecto piensa en **tokens**, pero en esta lección usamos un truco didáctico:

```python
token_counter=len
```

Así **cada mensaje completo cuenta como 1 token**. Si `max_tokens=4`, nos quedamos con los **4 últimos mensajes** (no 4 palabras sueltas).

### Parámetros que usamos

| Parámetro | Valor | Significado |
|-----------|--------|-------------|
| `strategy` | `"last"` | Conservar los últimos elementos (ventana al final del historial). |
| `max_tokens` | `4` (ejemplo) | Máximo de “tokens”; con `len`, máximo de mensajes. |
| `token_counter` | `len` | 1 mensaje = 1 unidad de recorte. |
| `start_on` | `"human"` | El recorte debe empezar en un mensaje de **usuario** (buena práctica en chat). |
| `include_system` | `True` | Si hay `SystemMessage` dentro de la lista, intentar conservarla al recortar. |

En nuestro código el **system prompt** lo añadimos aparte en el nodo (`SystemMessage` + `trimmed_messages`). Los mensajes en `state["messages"]` suelen ser solo `HumanMessage` y `AIMessage`.

### Uso en el nodo

```python
trimmer = trim_messages(...)
trimmed_messages = trimmer.invoke(state["messages"])
messages_for_llm = [SystemMessage(content=SYSTEM_PROMPT)] + trimmed_messages
response = llm.invoke(messages_for_llm)
```

---

## 4. `WindowedState`: ¿para qué sirve si es igual que `MessagesState`?

```python
class WindowedState(MessagesState):
    pass
```

No añade campos nuevos. Es una **convención de lectura**:

- Quien abre el código ve que este grafo usa **ventana deslizante**, no memoria ilimitada al LLM.
- El grafo se declara como `StateGraph(WindowedState)` en lugar de `StateGraph(MessagesState)`.

Por dentro sigue existiendo la clave **`messages`** y el mismo comportamiento de concatenar respuestas.

---

## 5. El grafo (igual estructura que la lección 3)

- Un nodo `chatbot`.
- `START → chatbot → END` (opcional pero claro).
- `MemorySaver` al compilar: misma idea de `thread_id` y checkpoints.

Lo que **cambia** es solo el interior de `chatbot_node` (el `trimmer`).

---

## 6. Prueba sugerida (como en el vídeo)

Ejecuta `main.py` y prueba esta secuencia:

1. *Hola, me llamo Santiago.*
2. Preguntas sobre Alemania (continente, habitantes, bandera…).
3. Sin repetir “Alemania”, pregunta por la bandera → debería inferir el país por el contexto **reciente**.
4. Pregunta *¿cómo me llamo?* → si ya pasaron más de **N** mensajes desde el saludo, es normal que **no recuerde** el nombre.

Cambia `MAX_MENSAJES_EN_VENTANA` en `main.py` (por ejemplo a 6) y repite: recordará un poco más hacia atrás, pero cada llamada será algo más cara.

---

## 7. Comparación rápida con la lección 3

| | Lección 3 (memoria completa al LLM) | Lección 4 (ventana deslizante) |
|---|-------------------------------------|--------------------------------|
| Estado en checkpoint | Historial completo | Historial completo |
| Lo que ve el LLM | Todo el historial | Últimos N mensajes |
| Recuerda nombre al inicio tras muchos turnos | Sí (hasta llenar contexto) | No, si salió de la ventana |
| Coste por llamada | Crece con la conversación | Acotado por N |

---

## 8. Cómo ejecutar

```powershell
cd "C:\Users\maria\Desktop\LangChain & LangGraph\5. Memoria y gestion del contexto\4. Memoria con ventana deslizante en LangGraph"
..\..\venv\Scripts\Activate.ps1
python main.py
```

Necesitas `OPENAI_API_KEY` en el `.env` de la raíz del curso.

---

## 9. Qué viene después

En la transcripción del curso se menciona un **artículo** con más tipos de memoria y, a continuación, **memoria persistente** (por ejemplo SQLite en lugar de solo RAM). La ventana deslizante se puede combinar con persistencia: guardas todo en disco, pero al LLM sigues mandando solo la ventana.

---

## 10. Resumen en una frase

**Guardamos el historial completo en el grafo, pero recortamos con `trim_messages` justo antes de llamar al LLM**, para controlar coste, contexto y lo que el modelo “recuerda” en cada turno.

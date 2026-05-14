# Memoria conversacional con LangGraph y `MemorySaver`

Esta lección es la continuación natural de la anterior, donde vimos memoria en LangChain con **`RunnableWithMessageHistory`**. Aquí vamos **mucho más despacio**: asumimos que LangGraph, los grafos y el estado son conceptos nuevos.

---

## 1. ¿Qué problema resolvemos?

Queremos un **chat en terminal** que:

1. Reciba lo que escribe el usuario.
2. Llame al modelo (por ejemplo, GPT con `ChatOpenAI`).
3. **Recuerde** lo dicho antes en la misma conversación (nombre, temas, etc.).

Eso es **memoria conversacional**: no basta con la última frase; el modelo necesita el **historial**.

---

## 2. Lo que ya sabíamos: memoria con LangChain

En la lección anterior usamos **`RunnableWithMessageHistory`**: LangChain envuelve una cadena (`prompt | llm`) y gestiona un historial por **`session_id`**.

- **Ventaja:** Código corto y directo para cadenas lineales.
- **Situación actual:** Sigue siendo válido; **no aparece como “deprecated”** solo por usarlo.

La documentación y el ecosistema **recomiendan encarecidamente** usar **LangGraph** cuando quieres **memoria, checkpoints y flujos** más controlables (incluso si la memoria es **solo en RAM** y se pierde al cerrar el programa).

> **Nota sobre la transcripción del vídeo:** a veces se escucha “Launchy” o “Landgraf”. En este material nos referimos siempre a **LangChain** y **LangGraph**.

---

## 3. Ideas nuevas: qué es un “grafo” en LangGraph (versión mínima)

Imagina una **mini-aplicación** dibujada con cajas y flechas:

- **Nodo:** una caja. Es una **función de Python** que hace un trabajo (aquí: “hablar con el LLM”).
- **Arista (edge):** una flecha que dice **después de qué nodo** sigue cuál.
- **`START`:** el punto de entrada del grafo (por dónde “entra” la ejecución).
- **`END`:** el punto en que el grafo **termina** (opcional en grafos muy simples; en nuestro código lo dejamos explícito para que veas el camino completo).

En esta lección el grafo es **de un solo nodo** (`chatbot`). Parece “exagerado” usar un grafo para eso, pero sirve para **aprender el patrón** que luego usarás con varios nodos, condiciones, herramientas, etc.

---

## 4. El “estado”: la caja común donde guardamos datos

En LangGraph, el **estado** es como una **variable compartida** que leen y actualizan los nodos.

- Cada nodo recibe el **estado actual**.
- Devuelve un **diccionario con solo lo que cambia** (actualización parcial); LangGraph lo **fusiona** con el estado anterior.

En nuestro ejemplo no definimos a mano una clase `TypedDict` con muchos campos: usamos un esquema ya pensado para chat.

---

## 5. `MessagesState`: estado “pre-hecho” para historial de mensajes

**`MessagesState`** es un tipo de estado **predefinido** en LangGraph pensado para conversación.

Lleva, entre otras cosas, una lista llamada **`messages`**:

- Ahí van entrando mensajes del **usuario** (`HumanMessage`) y del **modelo** (`AIMessage`), etc.
- Esa lista está preparada para que, al devolver nuevos mensajes desde un nodo, **no se borre todo el historial**, sino que los **nuevos se añadan** al historial existente (en la práctica, mediante un **reducer** interno; en el curso basta con saber: *“devuelvo la respuesta nueva y LangGraph la concatena al historial”*).

Por eso en el nodo hacemos algo equivalente a:

- Leer `state["messages"]` (todo lo que ya pasó).
- Construir la lista que verá el LLM: **instrucción de sistema** + historial.
- Llamar al modelo.
- Devolver `{"messages": [respuesta]}` para **actualizar** el estado con la última respuesta del asistente.

---

## 6. `StateGraph`: construir el grafo

**`StateGraph(...)`** es el constructor del grafo. Le indicamos **qué forma tiene el estado**; aquí: `MessagesState`.

Pasos típicos:

1. `workflow = StateGraph(MessagesState)` — crear el grafo vacío con ese esquema.
2. `workflow.add_node("chatbot", chatbot_node)` — registrar la función `chatbot_node` como nodo llamado `"chatbot"`.
3. `workflow.add_edge(START, "chatbot")` — la ejecución **empieza** en `chatbot`.
4. `workflow.add_edge("chatbot", END)` — después de `chatbot`, **termina** (recomendado para claridad; con un solo nodo a veces no hace falta, pero es buena costumbre).

---

## 7. Checkpoints y `MemorySaver`: “guardar fotos” del estado

**Checkpoint** (punto de control): en LangGraph es el mecanismo que **guarda el estado** del grafo tras los pasos de ejecución, asociado a un identificador de conversación (**`thread_id`**).

- Permite **reanudar** una conversación sin reconstruir tú a mano el historial en un diccionario Python.
- Permite depuración, trazas, etc. (según lo que configures).

**`MemorySaver`** es un **checkpointer en memoria RAM**:

- **Volátil:** si cierras el proceso o apagas el equipo, se pierde.
- **Misma sesión / mismo proceso:** mientras uses el **mismo `thread_id`**, LangGraph puede **recuperar** el estado guardado y seguir la conversación.

En lecciones o proyectos posteriores verás checkpointers **persistentes** (por ejemplo **SQLite**): misma idea (guardar estado por `thread_id`), pero sobrevive al reinicio.

---

## 8. Cómo encaja todo en cada mensaje del usuario (flujo mental)

Supón que ya hubo varios mensajes guardados para `thread_id = "sesion_terminal"`.

1. Llamas a `app.invoke(..., config)` con un **nuevo** `HumanMessage` del usuario.
2. LangGraph (gracias al checkpointer) **recupera** el estado previo de esa hebra (`thread_id`), en particular la lista `messages`.
3. El nodo `chatbot` arma **system + todos los mensajes** y llama al LLM.
4. El nodo devuelve la **nueva** respuesta del modelo como actualización de `messages`.
5. El checkpointer **vuelve a guardar** el estado actualizado en RAM.

Por eso el modelo puede responder a “¿cómo me llamo?” después de que dijeras “me llamo Santiago”: no es magia del `print`; es **estado + checkpoint + mismo `thread_id`**.

---

## 9. `thread_id` (LangGraph) vs `session_id` (LangChain)

- En **`RunnableWithMessageHistory`** solías ver `configurable: {"session_id": ...}`.
- En **LangGraph** con checkpointer lo habitual es **`thread_id`**: identifica **un hilo de conversación** (un chat, un usuario, un carrito de soporte, etc.).

En el código de ejemplo usamos un nombre tipo `sesion_terminal` como valor de `thread_id` para que sea fácil de leer en clase.

---

## 10. Comparación honesta con la lección anterior

| Aspecto | LangChain `RunnableWithMessageHistory` | LangGraph + `MessagesState` + `MemorySaver` |
|--------|------------------------------------------|---------------------------------------------|
| Enfoque | Cadena LCEL + historial gestionado | Grafo + estado + checkpoints |
| Memoria en RAM | Sí (según implementación del store) | Sí, con `MemorySaver` |
| Persistencia fuerte | Hay que cambiar el store | Cambiar el checkpointer (p. ej. SQLite) |
| Camino recomendado para agentes y flujos complejos | Limitado | Muy alineado con el ecosistema actual |

La **experiencia del usuario** en terminal puede parecer **idéntica** en los tres programas que veas en el curso; la **arquitectura** no lo es. LangGraph deja listo el terreno para **más nodos, ramas, human-in-the-loop**, etc.

> En la transcripción del vídeo se comenta que la respuesta puede **notarse más rápida** en este enfoque; depende del modelo, la red y el tamaño del historial. Lo importante didácticamente es **entender el flujo**, no comparar milisegundos en una demo.

---

## 11. Cómo ejecutar este ejemplo

Desde la carpeta de esta lección (con el `venv` del curso activado):

```powershell
cd "c:\Users\maria\Desktop\LangChain & LangGraph\5. Memoria y gestion del contexto\3. Memoria en LangGraph MemorySaver"
..\..\venv\Scripts\Activate.ps1
python main.py
```

Necesitas **`OPENAI_API_KEY`** en el `.env` de la **raíz del repositorio** del curso (el mismo que en otras lecciones).

Prueba sugerida (como en el vídeo):

1. “Hola, me llamo Santiago…”
2. “¿Cómo te llamas?”
3. “¿De qué te hablé antes?”
4. “¿Cómo me llamo?”

Si todo va bien, las respuestas usan **contexto previo** gracias al estado y al checkpointer.

---

## 12. Qué viene después (adelanto sin spoilear demasiado)

- Otros **tipos de memoria** y checkpointers **persistentes**.
- Mismo patrón de **`thread_id`**, pero sobreviviendo a reinicios.

Cuando domines este ejemplo de **un nodo**, los grafos con **varios nodos** serán solo “más cajas y más flechas” sobre la misma base de **estado + checkpoint**.

---

## 13. Resumen en una frase

**LangGraph + `MessagesState` + `MemorySaver`** nos da un chat con historial en RAM: el **estado** guarda los mensajes, el **checkpointer** los **recuerda entre invocaciones** del grafo mientras el **`thread_id`** sea el mismo y el proceso siga vivo.

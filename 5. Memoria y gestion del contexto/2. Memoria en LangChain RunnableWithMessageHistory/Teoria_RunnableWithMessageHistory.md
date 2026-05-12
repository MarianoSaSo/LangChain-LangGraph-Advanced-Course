# Gestión de Memoria Nativa con RunnableWithMessageHistory

En esta lección exploramos los métodos modernos que ofrece LangChain para gestionar la memoria de forma nativa, superando las limitaciones de los métodos manuales y las clases obsoletas.

---

## 1. El Estado Actual de la Memoria en LangChain

LangChain ha evolucionado rápidamente y actualmente nos encontramos en un momento de transición:

### ❌ Métodos Obsoletos (Legacy)
Es probable que encuentres código en internet usando clases como:
*   `ConversationBufferMemory`
*   `ConversationChain`

**Advertencia:** Aunque siguen funcionando, LangChain mostrará avisos de "Deprecation" (obsolescencia). Se recomienda **no utilizarlas** en proyectos nuevos, ya que serán eliminadas en versiones futuras.

### ✅ Enfoques Modernos Recomendados
1.  **LangGraph (Recomendado):** Es la solución más potente. Ideal para aplicaciones complejas que requieren control de flujo, persistencia en disco (base de datos) y gestión avanzada de estados.
2.  **RunnableWithMessageHistory:** Una solución nativa de LangChain para casos de uso más sencillos, prototipos o aplicaciones que no requieren persistencia a largo plazo (solo memoria RAM).

---

## 2. RunnableWithMessageHistory: Conceptos Clave

Esta clase permite "envolver" una cadena (Chain) estándar y añadirle capacidades de memoria de forma automática basándose en **identificadores de sesión**.

### Componentes Necesarios:

*   **`InMemoryChatMessageHistory`**: Un objeto que almacena los mensajes en la memoria volátil (RAM). 
    > [!WARNING]
    > Al apagar el programa o reiniciar el servidor, se pierde toda la información.
*   **`store`**: Un diccionario de Python que actúa como almacén central, organizando los historiales por `session_id`.
*   **`get_session_history`**: Una función auxiliar que recupera el historial correcto según el ID de sesión proporcionado.

---

## 3. Implementación Paso a Paso

### A. Definir el almacén y la función de búsqueda
```python
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
```

### B. Envolver la cadena original
Al crear el objeto `RunnableWithMessageHistory`, debemos indicarle qué variables del prompt corresponden al mensaje del usuario y cuál al historial.

```python
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",      # Variable de entrada
    history_messages_key="history"   # Variable del historial (Placeholder)
)
```

### C. Invocación con Sesiones
Para que la memoria funcione, debemos pasar un objeto `config` que contenga el `session_id`. Esto permite que varios usuarios interactúen con la misma aplicación sin que sus mensajes se mezclen (concurrencia).

```python
respuesta = chain_with_memory.invoke(
    {"input": "Hola, soy Santiago"},
    config={"configurable": {"session_id": "usuario_123"}}
)
```

---

## 4. Ventajas y Limitaciones

| Ventaja | Descripción |
| :--- | :--- |
| **Simplicidad** | Gestión automática del historial sin `extend()` manual. |
| **Sesiones** | Permite separar chats de diferentes usuarios fácilmente. |
| **Nativo** | Sigue los estándares modernos de LCEL. |

| Limitación | Descripción |
| :--- | :--- |
| **Volatilidad** | Los datos no persisten si se reinicia la aplicación. |
| **Escalabilidad** | Al usar memoria RAM, no es apto para millones de mensajes. |

---

> [!TIP]
> Si tu aplicación requiere que el usuario pueda volver días después y continuar la conversación, el siguiente paso es dar el salto a **LangGraph** para implementar persistencia en base de datos.

# 🎭 Lección: Creando los "Cerebros" del Grafo (Nodos y Lógica)

¡Bienvenidos! En esta lección vamos a aprender a construir los **nodos** de nuestro sistema de Helpdesk. 

Si el Grafo es el mapa de carreteras, los **Nodos** son las ciudades o estaciones donde ocurren cosas: donde se busca información, donde se toma una decisión o donde se redacta una respuesta.

---

## 1. La Estructura Principal: `HelpdeskGraph`

Para organizar nuestro código, metemos todo dentro de una clase. Imagina que esta clase es el "Libro de Instrucciones" de nuestro sistema.

```python
class HelpdeskGraph:
    """Grafo del sistema Helpdesk con Google Gemini."""

    def __init__(self):
        # 1. El Cerebro (LLM): Usamos Gemini para pensar.
        # Ponemos temperatura 0.1 para que sea preciso y no "alucine".
        self.llm = ChatGoogleGenerativeAI(model=CHAT_MODEL, temperature=0.1)
        
        # 2. La Biblioteca (RAG): Nuestro sistema de búsqueda de documentos.
        self.rag = VectorRAGSystem(chroma_path=CHROMADB_PATH)
        
        # 3. El Grafo: Aquí guardaremos la estructura final (de momento vacío).
        self.graph = None
```

> [!TIP]
> **¿Por qué temperatura 0.1?** 
> En un sistema de soporte no queremos que la IA sea creativa o cuente chistes. Queremos que sea seca, precisa y se ciña a los manuales técnicos.

---

## 2. Nodo 1: Procesar RAG (La Búsqueda)

La primera tarea de nuestro sistema es: *"Busca en mis manuales si hay algo que ayude a este usuario"*.

```python
def procesar_rag(self, state):
    """Busca el contexto de la consulta utilizando el sistema RAG."""
    consulta = state['consulta'] # Sacamos la duda del usuario del 'Estado'
    
    # Invocamos a nuestra 'Biblioteca' (RAG)
    resultado = self.rag.buscar(consulta)
    
    # Devolvemos un diccionario para ACTUALIZAR el estado
    return {
        "respuesta_rag": resultado["respuesta"],
        "confianza": resultado["confianza"],
        "fuentes": resultado["fuentes"],
        "contexto_rag": resultado["respuesta"],
        "historial": [
            f"RAG ejecutado correctamente",
            f"Confianza: {resultado['confianza']}",
            f"Fuentes halladas: {len(resultado['fuentes'])}"
        ]
    }
```

### 🧠 ¿Qué está pasando aquí?
1.  **Entrada:** Recibimos el `state` (la carpeta con toda la info del ticket).
2.  **Acción:** Llamamos a `self.rag.buscar`.
3.  **Salida:** Devolvemos los datos nuevos. LangGraph se encarga de "fusionar" esto con el estado anterior automáticamente.

---

## 3. Nodo 2: Clasificación (¿IA o Humano?)

Este es el nodo más inteligente. Aquí la IA lee lo que ha encontrado en el paso anterior y decide si puede resolverlo sola o si necesita "llamar a un jefe" (escalado humano).

```python
def clasificar_con_contexto(self, state):
    # Usamos .get() por seguridad: si no hay confianza, ponemos 0.
    consulta = state['consulta']
    contexto_rag = state.get('contexto_rag', '')
    confianza = state.get('confianza', 0)

    # El "Examen" que le pasamos a la IA
    prompt = ChatPromptTemplate.from_template("""
        Analiza esta consulta de helpdesk y decide si puede responderse automáticamente o necesita escalado:

        CONSULTA DEL USUARIO: {consulta}

        INFORMACIÓN ENCONTRADA EN LA BASE DE CONOCIMIENTO (GEMINI RAG):
        {contexto_rag}

        CONFIANZA DE LA BÚSQUEDA: {confianza}

        Criterios de decisión:
        - AUTOMATICO: Si la información de la BD responde completamente la consulta, 
          tiene buena confianza (>0.6), y es un tema estándar/procedimiento conocido
          
        - ESCALADO: Si la información es insuficiente, confianza baja, problema complejo/único,
          requiere acceso a sistemas internos, o involucra decisiones de negocio

        Responde solo con "automatico" o "escalado" y una breve justificación (máximo 20 palabras):
    """)
    
    # ... lógica de invocación ...
```

### 🛡️ Programación Defensiva: El `Try/Except`
A veces, internet falla o el modelo da un error. Por eso usamos un bloque de "seguridad":

```python
try:
    # Intentamos que la IA decida...
    # ...
except Exception as e:
    # Si la IA falla, tomamos una decisión de seguridad basada en el número de confianza.
    categoria = "automatico" if confianza >= 0.60 else "escalado"
    return {
        "categoria": categoria,
        "historial": [f"Error en IA, usando lógica de respaldo."]
    }
```

---

## 4. El "Historial" (El rastro de migas de pan)

Fíjate que en todos los nodos devolvemos una lista en `"historial"`. 

Gracias a que en nuestro `HelpdeskState` definimos esta variable así:
`historial: Annotated[List[str], add]`

LangGraph **no borra** el historial anterior, sino que **suma (add)** los mensajes nuevos. Es como una caja negra de un avión donde vamos anotando cada paso del proceso:
1. "Buscando en manuales..."
2. "Búsqueda con éxito (Confianza 0.8)..."
3. "IA clasifica como Automático..."

---

## 💡 Resumen para Estudiantes

1.  **Los Nodos son Funciones:** Reciben el estado actual y devuelven las piezas que quieren cambiar o añadir.
2.  **El Constructor:** Prepara las herramientas (Gemini, RAG, etc.).
3.  **Seguridad primero:** Siempre usamos `.get()` y `try/except` para que el programa no "explote" si falta un dato.
4.  **Historial:** Registramos todo lo que pasa para poder saber qué hizo la IA en cada momento.

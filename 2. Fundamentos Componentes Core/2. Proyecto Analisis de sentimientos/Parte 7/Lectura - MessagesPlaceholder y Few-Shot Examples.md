# MessagesPlaceholder y Few-Shot Examples

## ¿Qué es el In-Context Learning (ICL)?

El **In-Context Learning** o Aprendizaje en Contexto es la capacidad de los modelos de lenguaje de aprender nuevas tareas o patrones simplemente proporcionándoles ejemplos dentro del mismo prompt, sin necesidad de entrenar o ajustar el modelo (fine-tuning).

Es como mostrarle a alguien cómo hacer algo dándole ejemplos directos:
> "Mira, así se hace esto... y esto otro... ¿ahora puedes hacer tú algo similar?"

## ¿Qué son los Few-Shot Examples?

Los **Few-Shot Examples** (ejemplos de pocos intentos) son una técnica de ICL donde proporcionamos al modelo entre 2-10 ejemplos de la tarea que queremos que realice. Estos ejemplos sirven como "entrenamiento instantáneo".

### Estructura típica:
- **Sistema:** Instrucciones generales
- **Ejemplo 1:** Input → Output esperado
- **Ejemplo 2:** Input → Output esperado  
- **Ejemplo 3:** Input → Output esperado
- **Pregunta real:** Input actual → ?

## MessagesPlaceholder: La Herramienta Perfecta

`MessagesPlaceholder` es ideal para implementar few-shot examples porque:
- ✅ Mantiene la estructura de mensajes (`HumanMessage` / `AIMessage`)
- ✅ Permite insertar múltiples ejemplos dinámicamente
- ✅ El modelo entiende mucho mejor el formato natural de conversación
- ✅ Es fácil de reutilizar para diferentes tareas

---

## Evolución del Código: De Historial a Few-Shot

### Código Base (Historial de Conversación)
```python
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
 
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil que mantiene el contexto de la conversación."),
    MessagesPlaceholder(variable_name="historial"),
    ("human", "Usuario: {pregunta_actual}")
])
```

### Código Evolucionado (Few-Shot Examples)
```python
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
 
# Template para clasificación de sentimientos
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en análisis de sentimientos. Clasifica cada texto como: POSITIVO, NEGATIVO o NEUTRO."),
    MessagesPlaceholder(variable_name="ejemplos"),
    ("human", "Texto a analizar: {texto_usuario}")
])
 
# Array con pocos ejemplos (Few-shot examples)
ejemplos_sentimientos = [
    HumanMessage(content="Texto a analizar: Me encanta este producto, es increíble"),
    AIMessage(content="POSITIVO"),
    HumanMessage(content="Texto a analizar: El servicio fue terrible, muy decepcionante"),
    AIMessage(content="NEGATIVO"),
    HumanMessage(content="Texto a analizar: El clima está nublado hoy"),
    AIMessage(content="NEUTRO")
]
 
# Añadir la pregunta final pasándole los ejemplos
mensajes = chat_prompt.format_messages(
    ejemplos=ejemplos_sentimientos,
    texto_usuario="¡Qué día tan maravilloso!"
)
```

## Ventajas de Este Enfoque

**Con `MessagesPlaceholder`:**
- ✅ **Estructura clara:** Cada ejemplo mantiene su rol (`Human` o `AI`)
- ✅ **Escalable:** Fácil añadir/quitar ejemplos
- ✅ **Reutilizable:** Cambiar ejemplos = Nueva tarea
- ✅ **Natural:** El modelo procesa óptimamente el formato conversacional

**Sin `MessagesPlaceholder` (todo en texto plano):**
- ❌ **Menos claro:** Todo mezclado en un único string
- ❌ **Más errores:** El modelo puede confundirse de rol o de intenciones
- ❌ **Difícil mantenimiento:** Los cambios requieren reescribir y refactorizar todo
- ❌ **Menos efectivo:** Pierde la estructura conversacional natural del prompt

---

## Otros Ejemplos de Uso

### 1. Extracción de Información
```python
ejemplos_extraccion = [
    HumanMessage(content="Texto: Juan Pérez trabaja en Google como ingeniero desde 2020"),
    AIMessage(content="Nombre: Juan Pérez, Empresa: Google, Puesto: ingeniero, Año: 2020"),
    HumanMessage(content="Texto: María Silva es doctora en el Hospital Central"),
    AIMessage(content="Nombre: María Silva, Empresa: Hospital Central, Puesto: doctora, Año: N/A")
]
```

### 2. Traducción con Estilo
```python
ejemplos_traduccion = [
    HumanMessage(content="Formal en inglés: Good morning, how are you today?"),
    AIMessage(content="Casual en español: ¡Hola! ¿Qué tal?"),
    HumanMessage(content="Formal en inglés: I would like to schedule a meeting"),
    AIMessage(content="Casual en español: ¿Podemos quedar?")
]
```

---

## Mejores Prácticas
- **Cantidad ideal:** Utiliza de 2 a 5 ejemplos. Es suficiente para mostrar el patrón sin sobrecargar tokens o abrumar al LLM.
- **Ejemplos diversos:** Procura cubrir diferentes casos, variaciones o tipologías (como lo hicimos con un Positivo, Negativo y Neutro).
- **Formato consistente:** Emplea el mismo patrón de entrada-salida en todos los ejemplos.
- **Ejemplos de calidad:** Pásale outputs perfectos ya que servirán de referencia estricta de cómo el modelo imitará tu formato.

## Conclusión

El uso inteligente de `MessagesPlaceholder` transforma los **few-shot examples** de ser una técnica básica basada en inyectar gran texto, a posicionarse como una herramienta poderosa y flexible. 

Al emular una conversación de `HumanMessage` / `AIMessage`, el modelo comprende instantáneamente qué se espera de él, mejorando la precisión y el estilo visual de manera abismal.  ¡Esa es la magia del *In-Context Learning*! ✨

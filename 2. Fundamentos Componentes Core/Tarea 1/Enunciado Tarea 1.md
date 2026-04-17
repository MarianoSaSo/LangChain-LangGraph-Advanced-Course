# Tarea 1: Mejora tu Chatbot con ChatPromptTemplate, GPT y OpenAI

## 📋 Objetivo
En esta tarea transformarás tu chatbot del tema anterior para usar `ChatPromptTemplate` en lugar de `PromptTemplate`. Descubrirás las ventajas de trabajar con templates diseñados específicamente para modelos de chat y cómo estructurar prompts de forma más clara y eficiente.

> ⚠️ **Importante:** Esta tarea se centra en conceptos fundamentales de LangChain para aplicaciones conversacionales. Si encuentras dificultades, no te preocupes, el objetivo es que comprendas las diferencias entre ambos enfoques y sus casos de uso. La solución completa estará disponible al final de este artículo. ¡Experimenta y aprende las mejores prácticas!

---

## 🎯 Lo que aprenderás
- **ChatPromptTemplate:** Templates optimizados para modelos de chat.
- **Estructura de mensajes:** Roles de `System`, `Human`, y mensajes de IA en templates.
- **Separación clara:** Instrucciones del sistema *vs* conversación.
- **Mejores prácticas:** Cuándo usar cada tipo de template.
- **Optimización:** Aprovechamiento del formato nativo de chat de los LLMs.

---

## 🏁 Punto de partida
Tu código actual usa `PromptTemplate` y debería verse así:

```python
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate

# ... configuración de Streamlit ...

# Template actual con PromptTemplate
prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""Eres un asistente útil y amigable llamado ChatBot Pro. 

Historial de conversación:
{historial}

Responde de manera clara y concisa a la siguiente pregunta: {mensaje}"""
)

# Cadena actual
cadena = prompt_template | chat_model
```

---

## 🔄 ¿Por qué cambiar a `ChatPromptTemplate`?

**Problemas con `PromptTemplate`:**
- ❌ **Todo mezclado:** Instrucciones del sistema y conversación en un solo bloque de texto.
- ❌ **Menos claro:** Difícil separar qué es configuración y qué es conversación.
- ❌ **Menos natural:** No aprovecha la estructura nativa de chat de los modelos.
- ❌ **Mantenimiento difícil:** Cambios en las instrucciones requieren editar todo el template.

**Ventajas de `ChatPromptTemplate`:**
- ✅ **Estructura clara:** Separación entre mensajes del sistema, humanos y del asistente.
- ✅ **Mejor organización:** Cada tipo de mensaje tiene su propósito específico.
- ✅ **Más natural:** Aprovecha cómo están entrenados los modelos de chat.
- ✅ **Fácil mantenimiento:** Cambios independientes en cada sección.

---

## 🛠️ Implementación Paso a Paso

### 1. Actualizar Importaciones
Primer paso: Añadir las importaciones necesarias.

```python
# Añade esta importación a las existentes
from langchain.prompts import ChatPromptTemplate
```

### 2. Crear el ChatPromptTemplate
**Objetivo:** Reemplazar el `PromptTemplate` actual.

Reemplaza el template actual con este nuevo enfoque:

```python
chat_prompt = ChatPromptTemplate.from_messages([
    # Mensaje del sistema - Define la personalidad una sola vez
    ("system", "Eres un asistente útil y amigable llamado ChatBot Pro. Responde de manera clara y concisa."),
    
    # El historial y mensaje actual - se manejan como texto formateado
    ("human", "Historial de conversación:\n{historial}\n\nPregunta actual: {mensaje}")
])
```

**Diferencias clave:**
- `("system", "...")`: Define el comportamiento base del asistente (separado y claro).
- `("human", "...")`: Contiene el historial y la pregunta actual.
- **Estructura clara:** Cada mensaje tiene un rol específico.

### 3. Actualizar la Cadena
**Objetivo:** Usar el nuevo template en la cadena. Sigue siendo muy simple gracias a LCEL:

```python
cadena = chat_prompt | chat_model
```

### 4. Personalización del Sistema (Desafío)
**Objetivo:** Hacer el mensaje del sistema configurable desde tu barra lateral de Streamlit (`sidebar`).

```python
with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"])
    
    # ¡Nuevo! Personalidad configurable
    personalidad = st.selectbox(
        "Personalidad del Asistente",
        [
            "Útil y amigable",
            "Profesional y formal", 
            "Casual y relajado",
            "Experto técnico",
            "Creativo y divertido"
        ]
    )
    
    chat_model = ChatOpenAI(model=model_name, temperature=temperature)
    
    system_messages = {
        "Útil y amigable": "Eres un asistente útil y amigable llamado ChatBot Pro. Responde de manera clara y concisa.",
        "Profesional y formal": "Eres un asistente profesional y formal. Proporciona respuestas precisas y bien estructuradas.",
        "Casual y relajado": "Eres un asistente casual y relajado. Habla de forma natural y amigable, como un buen amigo.",
        "Experto técnico": "Eres un asistente experto técnico. Proporciona respuestas detalladas con precisión técnica.",
        "Creativo y divertido": "Eres un asistente creativo y divertido. Usa analogías, ejemplos creativos y mantén un tono alegre."
    }
    
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_messages[personalidad]),
        ("human", "Historial de conversación:\n{historial}\n\nPregunta actual: {mensaje}")
    ])
    
    cadena = chat_prompt | chat_model
```

---

## 💡 Conceptos Clave a Recordar

**Estructura de `ChatPromptTemplate`:**
```python
ChatPromptTemplate.from_messages([
    ("system", "Instrucciones base del asistente"),    # Configuración
    ("human", "Contenido del usuario + historial"),   # Datos de entrada
    ("assistant", "Respuesta anterior (opcional)")    # Para few-shot examples
])
```

**Roles de mensajes:**
- **system:** Instrucciones y configuración del comportamiento.
- **human:** Mensajes del usuario (incluyendo contexto/historial).
- **assistant:** Respuestas del modelo (para ejemplos o continuación de la conversación).

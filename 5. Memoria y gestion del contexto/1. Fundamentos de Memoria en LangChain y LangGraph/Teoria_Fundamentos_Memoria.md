# Fundamentos de Memoria y Gestión del Contexto en LLMs

La gestión de la memoria es uno de los aspectos más críticos y, a menudo, más ignorados al desarrollar aplicaciones con Modelos de Lenguaje de Gran Escala (LLMs) o Agentes de IA. En esta lección, exploraremos por qué es vital y cómo implementarla de forma básica.

---

## 1. ¿Por qué es importante la Memoria?

No se trata solo de que el chat "recuerde" nuestro nombre. Hay dos factores empresariales y técnicos fundamentales:

### A. La Ventana de Contexto (Context Window)
Cada modelo (como GPT-4o-mini) tiene un límite de información que puede procesar a la vez. Todo lo que enviamos al modelo ocupa espacio en esta "ventana".

### B. Optimización de Costes y Recursos
*   **Facturación:** Empresas como OpenAI cobran por la cantidad de información (tokens) enviada.
*   **Cómputo:** Más información en el contexto requiere más potencia de procesamiento y tiempo en los servidores de la nube.
*   **Eficiencia:** Una buena gestión de memoria evita enviar información irrelevante, ahorrando dinero y mejorando la velocidad de respuesta.

---

## 2. El Problema de la "Amnesia" de los LLMs

Por defecto, los LLMs son **stateless** (sin estado). Esto significa que cada mensaje que enviamos es tratado como el inicio de una conversación totalmente nueva.

> [!IMPORTANT]
> Si en el Mensaje 1 dices "Hola, me llamo Santiago" y en el Mensaje 2 preguntas "¿Cómo me llamo?", el modelo responderá que no lo sabe, porque en el segundo envío **no incluiste** el historial previo.

---

## 3. Implementación Rudimentaria (Manual)

Para solucionar esto, debemos enviar manualmente el historial en cada interacción. LangChain nos facilita esto mediante el uso de **MessagesPlaceholder**.

### El Flujo de Trabajo:
1.  **Definir un Placeholder:** En la plantilla del prompt, reservamos un espacio para el historial.
2.  **Mantener una Lista:** Creamos una lista en Python (`history = []`) para guardar los mensajes.
3.  **Actualizar:** Después de cada respuesta, añadimos tanto el mensaje del usuario como el del asistente a nuestra lista.

```python
# Ejemplo de placeholder en LangChain
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil."),
    MessagesPlaceholder(variable_name="historial"), # Espacio para el pasado
    ("human", "{input}") # El mensaje presente
])
```

---

## 4. Limitaciones del Método Manual

Aunque este método funciona para ejemplos sencillos, tiene graves desventajas para aplicaciones profesionales:

1.  **Crecimiento Indefinido:** La lista de mensajes crece sin parar, lo que eventualmente superará la "Ventana de Contexto" o disparará los costes.
2.  **Gestión de Sesiones:** En aplicaciones reales con múltiples usuarios, gestionar listas manuales para cada chat es complejo y propenso a errores (mezcla de conversaciones).
3.  **Falta de Estrategia:** No hay un criterio para "olvidar" información vieja o resumir conversaciones largas.

---

> [!TIP]
> En las próximas lecciones, aprenderemos cómo LangGraph y las herramientas avanzadas de LangChain automatizan esta gestión de forma profesional y escalable.

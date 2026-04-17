# Tema 2: Fundamentos y Componentes Core
## Lección 5: ChatPromptTemplate - Plantillas de prompts para chats

En la lección anterior vimos cómo construir nuestras plantillas base utilizando `PromptTemplate`. Aunque este mecanismo inicial es sumamente útil, en la práctica real puede limitarnos un poco, en especial cuando interactuamos con LLMs diseñados para **conversaciones y roles**.

### Limitaciones de un `PromptTemplate` clásico
Un `PromptTemplate` suele empaquetar todo el prompt en una cadena de texto enorme. En el ejercicio anterior, nosotros juntábamos:
1. **Instrucciones (Sistema):** *"Eres un experto en marketing."*
2. **Entrada interactiva (Humano/Usuario):** *"Sugiere un eslogan para: {producto}."*

Todo iba dentro del mismo bloque. Aunque esto nos sirva para una ejecución sencilla, cuando contamos con *root prompts* largos donde dictamos comportamientos muy detallados y restricciones específicas, agrupar las instrucciones base del modelo y la entrada libre del usuario en un mismo campo se vuelve confuso y propenso a errores (por ejemplo, vulnerabilidades de *Prompt Injection*).

### Introducción a `ChatPromptTemplate`
Para utilizar LLMs conversacionales en su máximo exponente, la mayoría de las veces recurriremos a la clase **`ChatPromptTemplate`**. 

Esta clase nos abre la puerta a poder definir una estructura de **lista de mensajes**, separando con claridad cristalina el propósito del texto basándose en los "roles" específicos (Sistema, Asistente, Humano). LLMs potentes como los de OpenAI están perfectamente entrenados para acatar estas distinciones.

#### ¿Cómo funciona `ChatPromptTemplate`?
En lugar de pasar un solo texto, la manera más habitual de construir esta clase es mediante el uso del método `.from_messages()`, empleando una lista de tuplas de la forma `("rol", "contenido del mensaje")`.

Veámoslo claro con código:

```python
from langchain_core.prompts import ChatPromptTemplate

# 1. Definimos la plantilla separando limpiamente los roles
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un traductor del español al inglés muy preciso."),
    ("human", "{texto}")
])

# 2. Componemos de antemano el mensaje probando nuestra variable 
mensajes = chat_prompt.format_messages(texto="Hola mundo, ¿cómo estás?")

# 3. Inspeccionamos cómo LangChain ha empaquetado cada bloque
for m in mensajes:
    print(f"{type(m)}: {m.content}")
```

### Anatomía del resultado generado
Al igual que en la clase anterior, la función `.format_messages()` **no** llama a nuestro modelo de IA todavía, sino que estructura los mensajes listos para ser consumidos por nuestro LLM.

La salida sería algo así:
```text
<class 'langchain_core.messages.system.SystemMessage'>: Eres un traductor del español al inglés muy preciso.
<class 'langchain_core.messages.human.HumanMessage'>: Hola mundo, ¿cómo estás?
```

Presta atención a lo que ocurrió automáticamente "bajo el capó":
1. Al especificar que el rol era `"system"`, LangChain castó esa cadena de texto y la envolvió en su clase equivalente: **`SystemMessage`**.
2. Al identificar el rol `"human"`, LangChain no solo reemplazó nuestra variable `{texto}` con la frase de prueba *"Hola mundo, ¿cómo estás?"*, sino que envolvió el resultado dentro de la estructura correspondiente: **`HumanMessage`**.

El sistema ahora comprende perfectamente qué parte debe tomar como un comportamiento ordenado por el código, y qué parte representa simplemente la interacción del usuario.

### Reto Práctico
Visto el mecanismo, te dejo como tarea un reto final:
> Toma este bloque de código base y finalízalo integrándole tu LLM (`ChatOpenAI` con el modelo *gpt-4o-mini*, por ejemplo). Conéctalos pasándole la plantilla de chat terminada y obtén la traducción real del texto al inglés.

¡Manos a la obra!

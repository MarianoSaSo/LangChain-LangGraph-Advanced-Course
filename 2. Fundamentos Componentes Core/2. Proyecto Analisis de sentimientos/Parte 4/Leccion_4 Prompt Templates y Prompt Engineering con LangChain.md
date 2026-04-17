# Tema 2: Fundamentos y Componentes Core
## Lección 4: Prompt Templates y Prompt Engineering con LangChain

En esta lección, vamos a explorar otro de los componentes fundamentales de LangChain: las **Plantillas de Prompts** (Prompt Templates). Ya vimos un adelanto de este concepto al final del tema anterior, pero ahora profundizaremos en su funcionamiento y buenas prácticas.

### ¿Qué son las Plantillas de Prompts?
Las plantillas de prompts son un mecanismo dentro de LangChain que nos permite estructurar fácilmente las instrucciones o preguntas que queremos realizar a los LLMs (Large Language Models). 

Su principal ventaja es que nos permiten separar y organizar dos tipos de información:
- **El contenido fijo:** Las instrucciones, roles o el contexto que proporcionamos siempre al modelo (ej. *"Eres un asistente útil y amigable..."* o *"Responde de manera clara y concisa"*).
- **El contenido variable:** El texto o los datos que cambian dinámicamente en cada ejecución, como una pregunta específica del usuario o el nombre de un producto.

### La importancia del Prompt Engineering
Crear buenas plantillas está estrechamente relacionado con la disciplina del **Prompt Engineering** (Ingeniería de Prompts). Aunque algunos llegaron a sugerir que esta disciplina desaparecería con la llegada de modelos más potentes (como GPT-4 y posteriores), la realidad ha demostrado lo contrario. 

La forma en que estructuramos, damos contexto y elaboramos nuestras instrucciones sigue determinando por completo la calidad y precisión del resultado de nuestros modelos. Por tanto, es vital iterar y validar continuamente nuestros prompts.

### Uso y comprobación de `PromptTemplate`
La clase básica que engloba este concepto en LangChain es `PromptTemplate` (importada desde `langchain_core.prompts`). 

A menudo, al construir cadenas complejas, le pasamos la plantilla directamente al LLM. Sin embargo, para asegurarnos de que nuestro "prompt engineering" sea efectivo, es muy útil poder comprobar **cómo se está componiendo el texto final** antes de enviarlo a un modelo, especialmente comprobando que las variables se inyectan exactamente donde queremos.

#### Ejemplo Práctico
En lugar de definir todo directamente dentro del constructor, una buena práctica es separar el proceso en pasos. Definimos el texto en una variable, inicializamos el objeto e inyectamos los valores simulados usando el método `.format()`.

```python
from langchain_core.prompts import PromptTemplate

# 1. Definimos el texto de la plantilla primero
template = "Eres un experto en marketing. Sugiere un eslogan creativo para un producto {producto}"

# 2. Construimos el objeto PromptTemplate
prompt = PromptTemplate(
    template = template,
    input_variables=["producto"]
)

# 3. Comprobamos cómo se llena la plantilla antes de usar un LLM
prompt_lleno = prompt.format(producto="café orgánico")

# Vemos el resultado
print(prompt_lleno)
```

Al ejecutar este código, obtenemos la validación de que nuestra cadena se ha armado correctamente, comprobando que el "placeholder" variable ha sido reemplazado por los datos enviados:
```text
Eres un experto en marketing. Sugiere un eslogan creativo para un producto café orgánico
```

### ¿Por qué es útil probar los prompts así?
En plantillas básicas de una sola línea, comprobar el resultado del método `.format()` puede parecer innecesario. Sin embargo, a medida que avancemos y utilicemos clases más específicas para Chat, mezclaremos mensajes con diferentes **roles** (Sistema, AI, Usuario) e insertaremos **historiales de conversación** completos. 

Es en esos escenarios complejos donde validar la correcta composición de la plantilla antes de interactuar con el LLM nos ahorrará muchos dolores de cabeza y nos permitirá depurar nuestros desarrollos de una forma mucho más eficaz.

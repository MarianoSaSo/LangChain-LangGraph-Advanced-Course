# Plantillas de mensajes con roles específicos

Para concluir con el bloque de plantillas de prompts, vamos a ver una técnica **avanzada** que nos ofrece LangChain para definir y organizar plantillas de manera modular, asignando plantillas concretas a roles específicos (como Sistema o Humano).

Aunque esta técnica no siempre se utilice en proyectos pequeños, resulta **especialmente útil en sistemas grandes y modulares**. Por ejemplo, cuando necesitas reutilizar plantillas de rol en múltiples componentes, o cuando deseas inyectar variables en partes específicas del sistema a lo largo de tu aplicación de forma constante.

## ¿Qué son las Plantillas basadas en roles?

En lugar de construir una plantilla gigante o usar simples pares de tuplas `("system", "...")` y `("human", "...")`, LangChain nos provee de clases con roles predefinidos:

* `SystemMessagePromptTemplate`: Para modelar el comportamiento general y las instrucciones del LLM.
* `HumanMessagePromptTemplate`: Para estructurar las preguntas o interacciones del usuario de manera estandarizada.

### 1. Plantilla de Sistema Modular

Podemos crear una plantilla base para el sistema con múltiples variables dinámicas:

```python
from langchain_core.prompts import SystemMessagePromptTemplate

plantilla_sistema = SystemMessagePromptTemplate.from_template(
    "Eres un {rol} especializado en {especialidad}. Responde de manera {tono}"
)
```

Esto es súper útil, porque si luego construimos una plataforma interactiva, el usuario podría cambiar la especialidad o elegir el tono (formal, escueto, extenso), y no tendríamos que reescribir la plantilla entera, simplemente cambiaríamos la variable `{tono}`.

### 2. Plantilla de Humano Modular

Asimismo, podemos estandarizar las entradas que realizan los usuarios. En lugar de pasar su "input" a secas, podemos inyectarle cierto contexto al enviarlo al LLM:

```python
from langchain_core.prompts import HumanMessagePromptTemplate

plantilla_humano = HumanMessagePromptTemplate.from_template(
    "Mi pregunta sobre {tema} es: {pregunta}"
)
```

## Componiendo el prompt final

La magia principal de LangChain nos la proporciona nuevamente `ChatPromptTemplate`. Gracias a él, podemos concatenar e integrar fácilmente un listado de `PromptTemplates` específicos.

Al combinarlos, mantenemos la jerarquía de los mensajes:

```python
from langchain_core.prompts import ChatPromptTemplate

# Componiendo múltiples plantillas
chat_prompt = ChatPromptTemplate.from_messages([
    plantilla_sistema,
    plantilla_humano
])
```
* **Nota:** Al ser modular, podríamos tener la plantilla de sistema definida en un fichero distinto de Python e importarla de manera global dentro de nuestro programa principal.

## Rellenar variables y renderizar 

Finalmente, utilizamos `format_messages` (o `invoke`) pasándole absolutamente todas las variables necesarias de las diferentes sub-plantillas:

```python
mensajes = chat_prompt.format_messages(
    rol="nutricionista",
    especialidad="dietas veganas",
    tono="profesional pero accesible",
    tema="proteínas vegetales",
    pregunta="¿Cuáles son las mejores fuentes de proteína vegana para un atleta profesional?"
)

for m in mensajes:
    print(m.content)
```

**Salida resultante:**
1. _Eres un nutricionista especializado en dietas veganas. Responde de manera profesional pero accesible._ (SystemMessage)
2. _Mi pregunta sobre proteínas vegetales es: ¿Cuáles son las mejores fuentes de proteína vegana para un atleta profesional?_ (HumanMessage)

## Conclusión

El uso de `SystemMessagePromptTemplate` y `HumanMessagePromptTemplate` nos brinda un ecosistema muy robusto para reutilizar partes de nuestro prompt. Las plantillas pueden aislarse, usarse repetidamente en diferentes partes de un proyecto y posteriormente ser ensambladas fácilmente en una plantilla final a través de `ChatPromptTemplate`.

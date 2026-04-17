# Lectura: PydanticOutputParser: El Método Clásico para salidas estructuradas

Antes de que LangChain introdujera el moderno método `with_structured_output()`, los desarrolladores usaban (y aún se usa extensamente) una clase llamada **`PydanticOutputParser`** para obtener respuestas estructuradas de los LLMs de manera consistente. 

Aunque es un método más *verboso* (requiere de configurar algunas cosas manualmente), sigue siendo muy usado en el mundo del desarrollo IA y resulta imprescindible para comprender los fundamentos de cómo funciona la estructuración de información (el Output Parsing).

---

## ¿Qué es PydanticOutputParser?

`PydanticOutputParser` es una clase concreta de LangChain que se encarga de convertir respuestas generadas en lenguaje natural y en texto plano a objetos Python estructurados, utilizando modelos de **Pydantic**. 

Su funcionamiento se basa en dos procesos concurrentes:
1. Extrae las descripciones de los campos del modelo Pydantic para autogenerar **instrucciones muy específicas de formato JSON** que inyecta dentro del *Prompt*.
2. Recibe el texto bruto en JSON que devuelve el LLM e, internamente, lo valida e instancia como objeto Pydantic retornándolo al final del bloque.

---

## Ejemplo Completo Paso a Paso

### Paso 1: Definir el Modelo Pydantic

De forma idéntica, definimos el formato de los datos que esperamos recibir heredando de `BaseModel`.
Es **obligatorio y crucial** añadir siempre detalladas descripciones en el `Field()`: el parser utilizará precisamente esta descripción para generar las reglas dinámicamente y enseñarle al modelo LLM qué le estamos pidiendo para ese valor.

```python
from pydantic import BaseModel, Field
 
class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Resumen breve del texto")
    sentimiento: str = Field(description="Sentimiento del texto (Positivo, neutro o negativo)")
    palabras_clave: list[str] = Field(description="Lista de palabras clave del texto")
```

### Paso 2: Crear el Parser

Con nuestro modelo subyacente de esquemas, instanciamos el Parser clásico.
```python
from langchain.output_parsers import PydanticOutputParser

# Crear el parser con nuestro modelo referenciado
parser = PydanticOutputParser(pydantic_object=AnalisisTexto)
 
# Si imprimiéramos parser.get_format_instructions()
# Veríamos exactamente cómo LangChain arma el prompt exigiéndole formato JSON.
```

### Paso 3: Crear el Prompt Template

La diferencia fundamental. Necesitamos colocar en nuestro template la variable reservada de instrucciones (`{format_instructions}`). Posteriormente, precargamos en él las que genera automáticamente nuestro Pydantic Parser utilizando el argumento `partial_variables` (útil para inyectar variables estáticas sin requerirlas en la ejecución con *invoke*):

```python
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""Eres un experto analista de texto. Analiza el siguiente texto con cuidado:
 
{format_instructions}
 
Texto a analizar:
{texto}
 
Análisis:""",
    input_variables=["texto"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
```

### Paso 4 y 5: Configurar LLM y encadenar

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3 # Baja temperatura (<0.5) ideal para salidas JSON predecibles sin "alucinaciones"
)

# Con LCEL, inyectamos el Prompt al LLM, y su resultado final se pasa por el Parser Pydantic.
chain = prompt | llm | parser
```

### Paso 6: Ejecutar el Análisis (Invoke)

Al mandar nuestro texto, todo el circuito se completa, retornando la instancia de clase de manera fiable.

```python
texto_prueba = "La nueva película de ciencia ficción es espectacular."
 
try:
    resultado = chain.invoke({"texto": texto_prueba})
    
    # Accedemos como propiedades del objeto
    print(f"Resumen: {resultado.resumen}")
    print(f"Sentimiento: {resultado.sentimiento}")
    
    # Exportamos un JSON estricto
    print(resultado.model_dump_json(indent=2))
    
except Exception as e:
    print(f"❌ Error durante el procesamiento: {e}")
```

---

## Conclusión

**PydanticOutputParser** sigue siendo en la actualidad una herramienta excepcionalmente robusta dentro de LangChain.
Aunque nos obliga a escribir Prompt y cadena LCEL para enlazarlo todo (mientras que `with_structured_output` lo esconde "mágicamente" de fondo), nos ofrece **control total** sobre nuestras instrucciones. 

Además, es imperativo utilizar este enfoque cuando integramos **modelos Open Source "clásicos"** o proveedores *Third-Party* que por el momento **no soportan el *Function Calling*** nativo (que es la tecnología que subyace debajo del otro método más moderno).

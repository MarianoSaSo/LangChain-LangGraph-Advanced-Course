# Estructurando Respuestas con LangChain y Pydantic

Existen diversas formas de crear *output parsers* con LangChain. Aunque hay métodos "antiguos" o tradicionales que consisten en definir clases para luego concatenarlas en una cadena mediante LCEL, actualmente existe una alternativa **mucho más sencilla, moderna y fiable**.

Este método consiste en aprovechar el poder de **Pydantic** junto a un método nativo que implementan los modelos de chat más recientes para asegurar salidas estructuradas.

---

## Implementación de salidas estructuradas (El método moderno)

Los modelos actuales en LangChain (como `ChatOpenAI`) implementan el método `with_structured_output()`. Este método permite indicar explícitamente la estructura de datos que nuestra aplicación necesita, y LangChain se encarga de indicárselo y validarlo por nosotros sin que lo tengamos que añadir manualmente al prompt.

### 1. Clases necesarias
Debemos importar `BaseModel` pero también **`Field`** desde Pydantic.
`Field` es extremadamente útil porque nos permite añadir una descripción a los campos de nuestro modelo, siendo clave para que el LLM entienda qué tipo de información o razonamiento se espera en cada atributo.

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
```

### 2. Definición del modelo Pydantic
Creamos nuestro modelo definiendo qué variables generará el LLM.

```python
class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Un resumen breve del texto")
    sentimiento: str = Field(description="El sentimiento del texto, debe ser positivo, neutro o negativo")
```
> Es posible definir otro tipos de datos como `int` o `float` en caso de requerir un dato numérico (y Pydantic / el LLM lo procesará para retornarlo con dicho formato exacto).

### 3. Crear el "Structured LLM"
A partir de un LLM base, creamos un nuevo LLM que fuerce este esquema:

```python
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6)

# Transforma el LLM para que la salida siempre sea la clase AnalisisTexto
structured_llm = llm.with_structured_output(AnalisisTexto) 
```

### 4. Invocación y resultados
Al utilizar el método `.invoke()`, recibiremos directamente una instancia de un objeto `BaseModel` de Pydantic (`AnalisisTexto`). ¡Sin necesidad de escribir prompts complejos diciendo que queremos el formato en JSON y con qué claves!

```python
texto_de_prueba = "Me encantó la nueva película de acción. Tiene muchos efectos especiales y emoción."
resultado = structured_llm.invoke(f"Analiza el siguiente texto: {texto_de_prueba}")

# 'resultado' es directamente nuestro objeto AnalisisTexto
print(resultado.model_dump_json())
# Imprime algo similar a: {"resumen":"...","sentimiento":"positivo"}
```

### Ventajas de utilizar este método:
1. **El objeto retornado NO es texto plano:** Nos devuelve una instancia real de Pydantic completamente lista para ser procesada en la lógica de nuestro código.
2. **Métodos nativos heredados:** Podemos utilizar métodos de `BaseModel` como `.model_dump_json()` para serializar los datos rápido a JSON, o simplemente usar los atributos del objeto (ej. `resultado.sentimiento`) directamente de manera "estricta".
3. **Simplicidad:** Reduce muchísimo código repetitivo *(boilerplate)* respecto a los parsers clásicos y mantiene los prompts mucho más limpios.

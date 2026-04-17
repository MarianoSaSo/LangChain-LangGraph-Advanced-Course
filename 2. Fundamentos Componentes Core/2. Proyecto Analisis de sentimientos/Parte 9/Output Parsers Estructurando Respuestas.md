# Output Parsers: Estructurando Respuestas

En las clases anteriores hablamos sobre los mecanismos que proporciona LangChain para elaborar prompts de manera óptima y dinámica. Sin embargo, hay un concepto igual de importante para crear aplicaciones con LangChain: los **Output Parsers** o procesadores de la salida.

## ¿Por qué necesitamos Output Parsers?
Cuando desarrollamos una aplicación que hace uso de LLMs, rara vez el texto en lenguaje natural que genera es el resultado directo que necesita nuestra aplicación en el back-end.

Lo habitual es que esa generación necesite procesarse o estructurarse (por ejemplo, en formato `JSON` o `CSV`) para que sirva de entrada para otro sistema, o para utilizar la información como si de un diccionario o una lista en Python se tratara, en lugar de un `string`. 

Los **Output Parsers** entran aquí para ayudarnos a forzar la salida de nuestro LLM a que tenga un formato específico, estructurado y con tipos de datos concretos ya preparados para las siguientes etapas de nuestro sistema.

LangChain nos provee de diferentes clases que podemos usar como parsers:
- `JsonOutputParser`
- `CsvOutputParser`
- `PydanticOutputParser` (uno de los más potentes e importantes para trabajar con datos complejos)

---

## Introducción a Pydantic
Antes de integrar Pydantic con LangChain, es importante entender qué es. **Pydantic** es una librería (externa e independiente de LangChain) que se utiliza exhaustivamente en Python para **validar y gestionar datos mediante modelos basados en type hints.**

Mediante clases en Python, especificamos qué datos esperamos recibir y en qué formato. Posteriormente, Pydantic se encarga de:
1. Validar si la información recibida es correcta.
2. Convertir o transformar los datos al tipo de dato que hemos especificado si no coinciden.
3. Rellenar campos faltantes con valores por defecto (si han sido definidos).

### Ejemplo práctico usando el modelo básico (`BaseModel`)

Creamos un modelo de datos `Usuario` en Pydantic:

```python
from pydantic import BaseModel

# Nuestro modelo debe de heredar siempre de BaseModel
class Usuario(BaseModel):
    identificador: int
    nombre: str
    activo: bool = True
```

Supongamos que recibimos la siguiente información de un sistema donde hay algunos fallos o faltan datos:

```python
datos_recuperados = {
    "identificador": "123", # En texto, en lugar de en formato numérico Entero
    "nombre": "Ana"
    # No proporciona si el usuario está activo o no
}
```

Al procesar esto con nuestro modelo Pydantic:

```python
usuario = Usuario(**datos_recuperados)
print(usuario)
# Salida: identificador=123 nombre='Ana' activo=True
```
Pydantic se ocupa automáticamente de convertir `"123"` a tipo Entero `123` y añade el campo `activo=True` porque no se encontraba en el objeto origen pero estaba establecido como valor por defecto.

También permite convertir el objeto ya estructurado a otros útiles formatos como JSON empleando `usuario.model_dump_json()`.

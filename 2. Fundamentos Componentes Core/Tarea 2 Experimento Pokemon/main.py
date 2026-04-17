import os
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

# Cargar variables de entorno
load_dotenv()

# 1. MODELO DE DATOS (Pydantic)
# Aquí definimos la "estructura perfecta" que queremos obtener.
# Heredamos de BaseModel para que Pydantic valide que todos los tipos de datos sean correctos.
# El parámetro "description" dentro de Field() es crucial: actúa como instrucción para el LLM.
class DatosPokemon(BaseModel):
    nombre: str = Field(description="Nombre del pokemon")
    numero: int = Field(description="Número en la Pokedex del pokemon")
    altura: float = Field(description="Altura del pokemon en metros")
    peso: float = Field(description="Peso del pokemon en kilogramos")
    tipo_pokemon: str = Field(description="Tipo principal y secundario de pokemon (ej. Fuego/Volador)")
    ataques: list[str] = Field(description="Lista de 3 a 5 ataques principales del pokemon")
    descripcion: str = Field(description="Breve descripción o curiosidad sobre el pokemon")
    debilidades: list[str] = Field(description="Lista de tipos contra los que es débil")
    fortalezas: list[str] = Field(description="Lista de tipos contra los que es fuerte")
    habilidades: list[str] = Field(description="Habilidades especiales del pokemon")
    # 'dict[str, int]' fuerza a responder con un diccionario de claves de texto y valores numéricos.
    estadisticas: dict[str, int] = Field(description="Diccionario con estadísticas base: hp, ataque, defensa, velocidad, etc.")
    imagen: str = Field(description="URL de la imagen oficial del pokemon proporcionada por PokeAPI")
    # Nota: Se ha eliminado un campo 'nombre' extra que estaba duplicado originalmente.
    evolucion: str = Field(description="Nombre de su siguiente evolución (o 'Ninguna' si no tiene)")

 
# 2. INSTANCIACIÓN DEL PARSER (PydanticOutputParser)
# El 'Parser' tiene dos misiones: 
# A) Generar un texto con reglas JSON muy estrictas para inyectar en el Prompt.
# B) Convertir el texto 'crudo' que devuelve el LLM a un objeto Pydantic de Python de verdad.
parser = PydanticOutputParser(pydantic_object=DatosPokemon)
 
# 3. CREACIÓN DEL PROMPT (Plantilla)
# Definimos el PromptTemplate con dos variables muy importantes:
# - {pokemon}: La variable dinámica que el usuario cambiará ("Pikachu", "Charizard", etc).
# - {format_instructions}: Aquí se inyectan automáticamente las instrucciones JSON gigantes que genera el Parser (paso 2).
prompt = PromptTemplate(
    template="""Actúa como una base de datos de la Pokédex. 
Busca información detallada y veraz sobre el siguiente Pokémon y proporciona un análisis estrictamente estructurado:
 
{format_instructions}
 
POKEMON SOLICITADO:
{pokemon}
 
RESPUESTA ESTRUCTURADA:""",
    input_variables=["pokemon"],
    # partial_variables pre-rellena {format_instructions} por nosotros. 
    # Así no tenemos que pasar las instrucciones manualmente cada vez que usamos la cadena.
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
 
# 4. MODELO DE LENGUAJE (LLM)
# Utilizamos gpt-4o-mini.
# Mantenemos la temperatura baja (0.2) porque no queremos que sea 'creativo'. 
# Queremos que sea preciso con los datos del Pokémon y estricto con la estructura JSON.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
 
# 5. CADENA LCEL (LangChain Expression Language)
# Encadenamos todo de manera elegante: 
# 1º Entra el nombre del Pokemon (diccionario) al 'prompt'.
# 2º El prompt (ya rellenado con el nombre y las instrucciones de formato) va al 'llm'.
# 3º La respuesta de texto del 'llm' va al 'parser', quien la transforma en el objeto Python apuntando a DatosPokemon.
chain = prompt | llm | parser
 
# 6. Ejecución del código
if __name__ == "__main__":
    pokemon = "Pikachu"
    
    print("\nIniciando análisis usando PydanticOutputParser...\n")
    try:
        resultado = chain.invoke({"pokemon": pokemon})
        
        print("✅ Análisis exitoso:\n")
        
        # Mostrar atributos directamente del objeto obtenido
        print("=== RESULTADOS COMO PROPIEDADES DEL OBJETO ===")
        print(f"Nombre: {resultado.nombre}")
        print(f"Numero: {resultado.numero}")
        print(f"Altura: {resultado.altura}")
        print(f"Peso: {resultado.peso}")
        print(f"Tipo: {resultado.tipo_pokemon}")
        print(f"Ataques: {', '.join(resultado.ataques)}")
        print(f"Descripcion: {resultado.descripcion}")
        print(f"Debilidades: {', '.join(resultado.debilidades)}")
        print(f"Fortalezas: {', '.join(resultado.fortalezas)}")
        print(f"Habilidades: {', '.join(resultado.habilidades)}")
        print(f"Estadisticas: {resultado.estadisticas}")
        print(f"Imagen: {resultado.imagen}")
        print(f"Evolucion: {resultado.evolucion}")
        
        # Exportar a JSON de manera confiable y con buen formato
        print("\n=== JSON RESULTANTE ===")
        print(resultado.model_dump_json(indent=2))

    except Exception as e:
        print(f"❌ Error durante el procesamiento: {e}")

"""
================================================================================
EXPLICACIÓN PARA ESTUDIANTES: ¿Qué hace get_format_instructions()?
================================================================================

Básicamente, este método traduce tu modelo de Pydantic (DatosPokemon) a un conjunto 
de instrucciones de texto muy detalladas que el modelo de lenguaje (LLM) puede entender.

En lugar de que tú tengas que escribir a mano en el Prompt: "Oye ChatGPT, devuélveme 
un JSON que tenga un campo 'nombre' que sea un string, un 'numero' que sea entero, 
una 'estadisticas' que sea un diccionario, etc...", este método lo hace automáticamente por ti.

¿Cómo funciona paso a paso en tu código?

1. Lee el modelo: El PydanticOutputParser analiza a fondo la clase DatosPokemon.
2. Extrae la estructura: Lee cada campo, el tipo de dato que esperas (ej. str, int, list[str], 
   dict[str, int]) y, muy importante, lee el texto que pusiste dentro de Field(description="...").
3. Genera las instrucciones: A partir de esa información, crea un bloque de texto gigante. 
   Si imprimieras el resultado de parser.get_format_instructions(), verías algo muy similar 
   a esto (en inglés, usualmente):

   "The output should be formatted as a JSON instance that conforms to the JSON schema below.
   
   As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]} 
   the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema.

   Here is the output schema:
   ```
   {"properties": {"nombre": {"title": "Nombre", "description": "Nombre del pokemon", "type": "string"}, "numero": {"title": "Numero", "description": "Número en la Pokedex del pokemon", "type": "integer"}, ... }}
   ```"
"""

import os
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

# Cargar variables de entorno
load_dotenv()

# 1. Modelo de datos Pydantic
class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Resumen breve del texto")
    sentimiento: str = Field(description="Sentimiento: Positivo, Neutro o Negativo")
    palabras_clave: list[str] = Field(description="3-5 palabras clave principales")
 
# 2. Instanciación del Parser clásico
parser = PydanticOutputParser(pydantic_object=AnalisisTexto)
 
# 3. Creación del Prompt (Inyectando las format_instructions generadas por el parser)
prompt = PromptTemplate(
    template="""Analiza este texto cuidadosamente y proporciona un análisis estructurado:
 
{format_instructions}
 
TEXTO:
{texto}
 
ANÁLISIS:""",
    input_variables=["texto"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
 
# 4. LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
 
# 5. Pipeline / Cadena LCEL
# El parser se concatena directamente al final para que formatee la respuesta texto del LLM
chain = prompt | llm | parser
 
# 6. Ejecución del código
if __name__ == "__main__":
    texto_prueba = "Me encantó la nueva película de acción, tiene efectos especiales increíbles y la trama mantiene la tensión en todo momento."
    
    print("\nIniciando análisis usando PydanticOutputParser...\n")
    try:
        resultado = chain.invoke({"texto": texto_prueba})
        
        print("✅ Análisis exitoso:\n")
        
        # Mostrar atributos directamente del objeto obtenido
        print("=== RESULTADOS COMO PROPIEDADES DEL OBJETO ===")
        print(f"Resumen: {resultado.resumen}")
        print(f"Sentimiento: {resultado.sentimiento}")
        print(f"Palabras clave: {', '.join(resultado.palabras_clave)}")
        
        # Exportar a JSON de manera confiable y con buen formato
        print("\n=== JSON RESULTANTE ===")
        print(resultado.model_dump_json(indent=2))

    except Exception as e:
        print(f"❌ Error durante el procesamiento: {e}")

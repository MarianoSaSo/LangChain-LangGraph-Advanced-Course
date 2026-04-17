import os
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# Cargar variables de entorno
load_dotenv()

# 1. Definición del modelo personalizado utilizando Pydantic
class AnalisisTexto(BaseModel):
    # Field permite añadir una descripción para que el LLM sepa qué debe generar
    resumen: str = Field(description="Un resumen breve del texto")
    sentimiento: str = Field(description="El sentimiento del texto. Debe ser positivo, neutro o negativo")

# 2. Instanciación del LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6)

# 3. Transformación del LLM para que tenga salidas estructuradas
# Le pasamos nuestro modelo de Pydantic al método
structured_llm = llm.with_structured_output(AnalisisTexto)

# 4. Invocación del modelo con una reseña de prueba
texto_de_prueba = "Me encantó la nueva película de acción. Tiene muchos efectos especiales y emoción."

# ¡Fíjate que ya no le pedimos que conteste en JSON en el prompt!
resultado = structured_llm.invoke(f"Analiza el siguiente texto: {texto_de_prueba}")

# 5. Comprobación del resultado
print("--- Objeto Pydantic instanciado ---")
print(type(resultado))
print(resultado)

print("\n--- Resultado exportado a formato JSON ---")
print(resultado.model_dump_json())

print("\n--- Acceso directo a atributos ---")
print("Resumen:", resultado.resumen)
print("Sentimiento:", resultado.sentimiento)
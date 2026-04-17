from pydantic import BaseModel, Field
from typing import List

class Flashcard(BaseModel):
    """Modelo para una tarjeta de estudio individual"""
    pregunta: str = Field(description="La pregunta clara y concisa basada en el contenido del estudio")
    respuesta: str = Field(description="La respuesta detallada pero enfocada para que el estudiante aprenda el concepto")
    concepto_clave: str = Field(description="El término o concepto principal que se está evaluando")

class FlashcardSet(BaseModel):
    """Modelo para una colección de tarjetas de estudio"""
    cards: List[Flashcard] = Field(description="Lista de tarjetas de estudio generadas")
    tema_general: str = Field(description="El tema principal identificado en el documento")

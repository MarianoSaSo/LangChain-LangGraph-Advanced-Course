from pydantic import BaseModel, Field
from typing import List, Optional

class JobMatch(BaseModel):
    """Modelo para una oferta de empleo encontrada y analizada"""
    titulo: str = Field(description="Título del puesto de trabajo")
    empresa: str = Field(description="Nombre de la empresa (si está disponible)")
    ubicacion: str = Field(description="Ciudad o modalidad (Remoto/Hibrido)")
    enlace: str = Field(description="URL directa a la oferta de trabajo")
    descripcion_corta: str = Field(description="Resumen breve de la oferta (máximo 100 caracteres)")
    compatibilidad: int = Field(description="Puntuación de 0 a 100 indicando qué tan bien encaja con el CV")
    razon: str = Field(description="Breve explicación de por qué esta oferta es ideal para el usuario")
    carta_presentacion: str = Field(description="Una carta de presentación ultra-personalizada redactada para esta oferta específica y este CV del candidato")


class JobSearchResponse(BaseModel):
    """Modelo para la lista de ofertas comparadas"""
    ofertas: List[JobMatch] = Field(description="Lista de las mejores ofertas encontradas y puntuadas")
    perfil_extraido: str = Field(description="Resumen de cómo la IA ha entendido el perfil profesional del usuario")

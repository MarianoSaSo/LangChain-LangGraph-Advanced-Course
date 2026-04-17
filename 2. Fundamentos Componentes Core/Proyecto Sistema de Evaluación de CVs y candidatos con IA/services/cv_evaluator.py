from langchain_openai import ChatOpenAI
from models.cv_model import AnalisisCV
from prompts.cv_prompts import crear_sistema_prompts
from utils.logger import logger
import time

def crear_evaluador_cv():
    modelo_base = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2
    )

    modelo_estructurado = modelo_base.with_structured_output(AnalisisCV)
    chat_prompt = crear_sistema_prompts()
    cadena_evaluacion = chat_prompt | modelo_estructurado

    return cadena_evaluacion

def evaluar_candidato(texto_cv: str, descripcion_puesto: str) -> AnalisisCV:
    try:
        logger.info("🤖 Iniciando cadena de evaluación del LLM...")
        inicio = time.time()
        
        cadena_evaluacion = crear_evaluador_cv()

        resultado = cadena_evaluacion.invoke({
            "texto_cv": texto_cv,
            "descripcion_puesto": descripcion_puesto
        })

        fin = time.time()
        duracion = fin - inicio
        
        logger.info(f"✨ Evaluación finalizada en {duracion:.2f} segundos.")
        logger.info(f"📊 Candidato: {resultado.nombre_candidato} | Ajuste: {resultado.porcentaje_ajuste}%")

        return resultado
    
    except Exception as e:
        logger.error(f"❌ Error interno evaluando CV: {e}")
        return AnalisisCV(
            nombre_candidato="Error en procesamiento.",
            experiencia_años=0,
            habilidades_clave=["Error al procesar CV"],
            education="No se puede determinar.",
            experiencia_relevante="Error durante el análisis.",
            fortalezas=["Requiere revisión manual del CV"],
            areas_mejora=["Verificar formato y legibilidad del PDF"],
            porcentaje_ajuste=0
        )


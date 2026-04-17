from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
import json
from dotenv import load_dotenv

# Cargar las variables de entorno (como OPENAI_API_KEY)
load_dotenv()

# =========================================================
# 1. Configuración del modelo
# =========================================================
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# =========================================================
# 2. Preprocesador de Texto
# =========================================================
def preprocess_text(text):
    """Limpia el texto eliminando espacios extras y limitando longitud"""
    return text.strip()[:500]

preprocessor = RunnableLambda(preprocess_text)

# =========================================================
# 3. Rama 1: Generación de Resumen
# =========================================================
def generate_summary(text):
    """Genera un resumen conciso del texto"""
    prompt = f"Resume en una sola oración: {text}"
    response = llm.invoke(prompt)
    return response.content

summary_branch = RunnableLambda(generate_summary)

# =========================================================
# 4. Rama 2: Análisis de Sentimientos
# =========================================================
def analyze_sentiment(text):
    """Analiza el sentimiento y devuelve un resultado estructurado en JSON"""
    prompt = f"""Analiza el sentimiento del siguiente texto.
    Responde ÚNICAMENTE en formato JSON válido:
    {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve"}}
    
    Texto: {text}"""
    
    response = llm.invoke(prompt)
    try:
        # Limpieza por si el modelo responde envuelto en markdown (```json ... ```)
        cleaned_response = response.content.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "Error en análisis"}
    
sentiment_branch = RunnableLambda(analyze_sentiment)

# =========================================================
# 5. Fusión de Resultados
# =========================================================
def merge_results(data):
    """Combina los resultados de ambas ramas en un formato unificado"""
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }

merger = RunnableLambda(merge_results)

# =========================================================
# 6. Ejecución en Paralelo (El cambio más importante)
# =========================================================
# RunnableParallel ejecuta 'summary_branch' y 'sentiment_branch' a la vez.
# Envía de forma paralela la misma entrada a ambas funciones.
parallel_analysis = RunnableParallel({
    "resumen": summary_branch,
    "sentimiento_data": sentiment_branch
})

# =========================================================
# 7. Cadena Completa
# =========================================================
# Usamos el operador (|) para canalizar los pasos (pipeline)
chain = preprocessor | parallel_analysis | merger

# =========================================================
# 8. Probando el Sistema
# =========================================================
if __name__ == "__main__":
    textos_prueba = [
        "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido.",
        "El servicio al cliente fue terrible, nadie me ayudó con mi problema.",
        "El clima está nublado hoy, probablemente llueva más tarde."
    ]
    
    for texto in textos_prueba:
        resultado = chain.invoke(texto)
        print(f"Texto: {texto}")
        print(f"Resultado: {json.dumps(resultado, indent=2, ensure_ascii=False)}")
        print("-" * 50)

from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# =========================================================
# 1. Configuración del modelo
# =========================================================
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# =========================================================
# 2. Preprocesador
# =========================================================
def preprocess_text(text):
    """Limpia el texto eliminando espacios extras y limitando longitud"""
    return text.strip()[:500]

preprocessor = RunnableLambda(preprocess_text)

# =========================================================
# 3. Generación de resumen (Rama 1)
# =========================================================
def generate_summary(text):
    """Genera un resumen conciso del texto"""
    prompt = f"Resume en una sola oración: {text}"
    response = llm.invoke(prompt)
    return response.content

summary_branch = RunnableLambda(generate_summary)

# =========================================================
# 4. Análisis de sentimiento (Rama 2)
# =========================================================
def analyze_sentiment(text):
    """Analiza el sentimiento y devuelve resultado estructurado"""
    prompt = f"""Analiza el sentimiento del siguiente texto.
    Responde ÚNICAMENTE en formato JSON válido:
    {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve"}}
    
    Texto: {text}"""
    
    response = llm.invoke(prompt)
    try:
        # Limpieza para que no falle si responde en formato Markdown
        cleaned_response = response.content.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "Error en análisis"}

sentiment_branch = RunnableLambda(analyze_sentiment)

# =========================================================
# 5. Combinación de resultados
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
# 6. Ejecución Paralela y Cadena
# =========================================================
parallel_analysis = RunnableParallel({
    "resumen": summary_branch,
    "sentimiento_data": sentiment_branch
})

# Cadena completa
chain = preprocessor | parallel_analysis | merger

# =========================================================
# 7. Procesamiento por Lotes (Batch)
# =========================================================
if __name__ == "__main__":
    # Conjunto (batch) de reseñas a procesar al mismo tiempo (Lotes)
    reviews_batch = [
        "Excelente producto, muy satisfecho con la compra",
        "Terrible calidad, no lo recomiendo para nada",
        "Está bien, cumple su función básica pero nada especial"
    ]

    # Ejecutamos la cadena usando .batch() en lugar de .invoke()
    resultado_batch = chain.batch(reviews_batch)

    # Imprimiendo el resultado de manera ordenada
    print("Resultados del procesamiento por lote (Batch):\n")
    print(json.dumps(resultado_batch, indent=2, ensure_ascii=False))

from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
import json
from dotenv import load_dotenv

# Cargar las variables de entorno (como OPENAI_API_KEY)
load_dotenv()

# =========================================================
# 1. Configuración del modelo
# =========================================================
# Usamos temperature=0 para obtener respuestas más deterministas y consistentes
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# =========================================================
# 2. Preprocesador de Texto
# =========================================================
def preprocess_text(text):
    """Limpia el texto eliminando espacios extras y limitando longitud"""
    # Usamos strip() para limpiar márgenes  (es decir, el principio y el final) y [:500] para evitar textos muy largos
    return text.strip()[:500]

# Convertimos la función en un Runnable
preprocessor = RunnableLambda(preprocess_text)

# =========================================================
# 3. Generador de Resúmenes
# =========================================================
def generate_summary(text):
    """Genera un resumen conciso del texto"""
    prompt = f"Resume en una sola oración: {text}"
    response = llm.invoke(prompt)
    return response.content

# =========================================================
# 4. Analizador de Sentimientos
# =========================================================
def analyze_sentiment(text):
    """Analiza el sentimiento y devuelve resultado estructurado"""
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
        # Manejo de errores por si el modelo falla al responder en JSON válido
        return {"sentimiento": "neutro", "razon": "Error en análisis"}

# =========================================================
# 5. Función de Combinación
# =========================================================
def merge_results(data):
    """Combina los resultados de ambas ramas en un formato unificado"""
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }

# =========================================================
# 6. Función de Procesamiento Principal
# =========================================================
def process_one(t):
    resumen = generate_summary(t)              # Llamada 1 al LLM
    sentimiento_data = analyze_sentiment(t)    # Llamada 2 al LLM
    
    # Combinamos usando la función que creamos
    return merge_results({
        "resumen": resumen,
        "sentimiento_data": sentimiento_data
    })

# Convertir en Runnable
process = RunnableLambda(process_one)

# =========================================================
# 7. Construcción de la Cadena Final
# =========================================================
# La cadena completa combinando preprocesamiento y orquestación con pipeline (|)
chain = preprocessor | process

# =========================================================
# 8. Probando tu Sistema
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

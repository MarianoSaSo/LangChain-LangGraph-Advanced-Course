import os
import numpy as np
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# =====================================================================
# 1. Cargar variables de entorno (Como nuestra Google API Key)
# =====================================================================
load_dotenv()

# =====================================================================
# Función Helper: Calcular la similitud del coseno entre dos vectores
# =====================================================================
def calcular_similitud_coseno(v1, v2):
    """
    Calcula el 'Cosine Similarity' usando numpy.
    Un valor cercano a 1 indica alta similitud semántica.
    """
    producto_punto = np.dot(v1, v2)
    norma_v1 = np.linalg.norm(v1)
    norma_v2 = np.linalg.norm(v2)
    return producto_punto / (norma_v1 * norma_v2)


def main():
    print("🌟 Iniciando Lección de Embeddings con Google Gemini...\n")

    # =====================================================================
    # 2. Inicializar el modelo de Embeddings
    # =====================================================================
    # Utilizamos el modelo embedding de Gemini: 'models/gemini-embedding-001'
    # (dependiendo de tu región o tipo de API Key, a veces es el equivalente a text-embedding-004)
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    # Definimos los textos que vamos a evaluar.
    texto_1 = "La capital de Francia es París."
    texto_2_similar = "París es la ciudad capital de Francia."
    texto_2_diferente = "París es un nombre común para mascotas."

    # =====================================================================
    # 3. Generar los Embeddings (Vectores) para nuestros textos
    # =====================================================================
    # Convertimos nuestros textos al espacio vectorial
    vector_1 = embeddings_model.embed_query(texto_1)
    vector_2_similar = embeddings_model.embed_query(texto_2_similar)
    vector_2_diferente = embeddings_model.embed_query(texto_2_diferente)

    # Observamos la 'dimensión' del vector, todos los vectores tienen la misma dimension, cogemos uno al azar.
    dimension = len(vector_1)
    print(f"📏 Dimensión de los vectores generados (Google): {dimension} valores.\n")

    # =====================================================================
    # 4. Calcular y observar las medidas de similitud
    # =====================================================================
    print("=" * 60)
    print("🎯 CASO 1: Textos Semánticamente Similares")
    print("=" * 60)
    print(f"Texto 1: '{texto_1}'")
    print(f"Texto 2: '{texto_2_similar}'")
    
    similitud_alta = calcular_similitud_coseno(vector_1, vector_2_similar)
    print(f"Similitud de coseno: {similitud_alta:.4f} (Se acerca a 1.0 = Muy similar)\n")


    print("=" * 60)
    print("🎯 CASO 2: Textos Semánticamente Diferentes")
    print("=" * 60)
    print(f"Texto 1: '{texto_1}'")
    print(f"Texto 2: '{texto_2_diferente}'")
    
    similitud_baja = calcular_similitud_coseno(vector_1, vector_2_diferente)
    print(f"Similitud de coseno: {similitud_baja:.4f} (Mucho menor que el primero)\n")

    print("💡 Conclusión:")
    print("Los Embeddings logran captar el VERDADERO significado y contexto de los textos.")


if __name__ == "__main__":
    main()
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 0. Configuración del entorno
# Cargamos las variables del .env (especialmente OPENAI_API_KEY)
load_dotenv()

def leccion_text_splitters():
    # --- 🛠️ MEJORA DE RUTA (SOLUCIONA EL ERROR DE ARCHIVO NO ENCONTRADO) ---
    # Obtenemos la ruta absoluta de la carpeta donde se encuentra este script actual
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    # Unimos esa carpeta con el nombre del PDF para que siempre sea localizable
    pdf_path = os.path.join(directorio_actual, "quijote.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"⚠️ Error: No se ha encontrado el archivo {pdf_path}.")
        print("💡 TIP: Asegúrate de que el PDF y el main.py estén en la misma carpeta.")
        return

    print(f"📄 Cargando documento desde: {pdf_path}...")
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    # 1. Combinar todas las páginas en un texto único
    full_text = ""
    for page in pages:
        full_text += page.page_content + "\n"

    total_caracteres = len(full_text)
    print(f"📊 El documento completo tiene: {total_caracteres} caracteres.")
    
    # ---------------------------------------------------------
    # PARTE 1: El Error (Por qué necesitamos splitters)
    # ---------------------------------------------------------
    # Para demostrar el error real en clase, cambia demostrar_error a True
    demostrar_error = False 
    
    if demostrar_error:
        print("\n🤖 Intentando enviar el documento completo al LLM (GPT-4o-mini)...")
        # Este modelo tiene 128k de context window, pero enviar todo el Quijote suele superarlo
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        try:
            llm.invoke(f"Resume este libro: {full_text}")
        except Exception as e:
            print(f"❌ ERROR DETECTADO (Limite de contexto): {e}")

    # ---------------------------------------------------------
    # PARTE 2: La Solución (Text Splitters)
    # ---------------------------------------------------------
    print("\n✂️ Aplicando división inteligente de texto (Text Splitters)...")

    # Configuramos el splitter más usado de LangChain: el "RecursiveCharacter"
    # Este splitter busca cortes orgánicos (párrafos, saltos de línea, espacios)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,    # Cada fragmento tendrá aprox 1200 caracteres
        chunk_overlap=200,  # 200 caracteres de solapamiento para no perder contexto
        length_function=len # Usamos la longitud de caracteres (standard)
    )

    # Dividimos el texto en una lista de fragmentos (Strings)
    chunks = text_splitter.split_text(full_text)

    # ---------------------------------------------------------
    # RESULTADOS
    # ---------------------------------------------------------
    print(f"✅ ¡Éxito! El libro se ha dividido en {len(chunks)} fragmentos manejables.")
    
    print("\n--- Vista previa de los fragmentos (Educativo) ---")
    for i, chunk in enumerate(chunks[:3]):
        # Mostramos una previsualización de los primeros 3 trozos
        print(f"\n🔹 Fragmento {i+1} (Longitud: {len(chunk)}):")
        print(f"{chunk[:250]}...") # Mostramos un pequeño anticipo
        print("-" * 40)

if __name__ == "__main__":
    leccion_text_splitters()
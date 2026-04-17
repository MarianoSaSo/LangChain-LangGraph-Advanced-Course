import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
# Cambiamos ChatOpenAI por ChatGoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 0. Cargar variables de entorno (claves de API)
load_dotenv()

def leccion_recursive_splitter():
    # 1. Cargar el documento PDF
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(directorio_actual, "quijote.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"⚠️ Error: No se ha encontrado el archivo {pdf_path}.")
        return

    print("📄 Cargando el documento completo...")
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    # 2. Dividir el texto en chunks más pequeños
    print("\n✂️ Configurando el RecursiveCharacterTextSplitter...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(pages)
    print(f"✅ Documento dividido en {len(chunks)} fragmentos útiles (chunks).")

    # 3. Procesar cada chunk con un modelo gratuito (Gemini 2.5 Flash)
    print("\n🤖 Iniciando análisis con el modelo gratuito de Google (Gemini 2.5 Flash)...")
    
    # Hemos sustituido ChatOpenAI por ChatGoogleGenerativeAI
    # Usamos Gemini 2.5 Flash ya que es el modelo gratuito más actual disponible en tu cuenta.
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
    
    summaries = [] 
    MAX_CHUNKS_A_PROCESAR = 5 # Bajamos a 5 por ser la capa gratuita y no saturar las peticiones.
    
    for i, chunk in enumerate(chunks):
        if i >= MAX_CHUNKS_A_PROCESAR:
            print(f"🛑 Deteniendo el proceso en el fragmento {i} para ahorrar tiempo de API.")
            break
            
        print(f"⏳ Procesando fragmento {i+1}/{MAX_CHUNKS_A_PROCESAR}...")
        
        prompt = f"Haz un resumen de los puntos mas importantes del siguiente texto:\n\n{chunk.page_content}"
        response = llm.invoke(prompt)
        summaries.append(response.content)

    if not summaries:
        print("⚠️ No hay resúmenes para procesar.")
        return

    print("\n🧠 Generando el resumen final unificado...\n")
    texto_resumenes = " ".join(summaries)
    
    prompt_final = f"Combina y sintetiza estos resumenes en un resumen coherente y completo:\n\n{texto_resumenes}"
    final_summary = llm.invoke(prompt_final)
    
    print("================== RESUMEN FINAL (GEMINI) ==================")
    print(final_summary.content)
    print("============================================================\n")

if __name__ == "__main__":
    leccion_recursive_splitter()
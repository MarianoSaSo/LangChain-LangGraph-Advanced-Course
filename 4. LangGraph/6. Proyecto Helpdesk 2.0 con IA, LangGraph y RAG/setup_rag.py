import hashlib #crear IDs únicos
import shutil # Borrar carpetas
from typing import List # Para decir “esto es una lista” (tipado)
from pathlib import Path # Para manejar rutas de archivos de forma inteligente
from langchain_community.document_loaders import DirectoryLoader, TextLoader # Para cargar documentos
from langchain_community.vectorstores import Chroma # Para crear la base de datos vectorial
from langchain_google_genai import GoogleGenerativeAIEmbeddings # Para crear los embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter # Para dividir los documentos
from langchain_core.documents import Document # Para crear los documentos

# Importamos las variables de configuración de nuestro archivo externo
from config import * 

class DocumentProcessor:
    """
    Clase DocumentProcessor: Se encarga de transformar nuestra base de conocimientos
    (archivos Markdown) en vectores almacenables en una base de datos vectorial
    utilizando Google Gemini Embeddings.
    """
    
    def __init__(self, docs_path: str = DOCS_PATH, chroma_path: str = CHROMADB_PATH):
        # 1. Rutas de carpetas: Las convertimos a objetos Path para que funcionen en cualquier SO (Windows/Mac/Linux)
        self.docs_path = Path(docs_path)
        self.chroma_path = Path(chroma_path)
        
        # 2. Motor de Inteligencia: Instanciamos el modelo de Google que convertirá texto en 
        # listas de números (vectores) llamadas 'embeddings'.
        self.embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDINGS_MODEL)
        
        # 3. La "Cizalla" (Splitter): Define cómo cortaremos los textos largos.
        # - chunk_size: ¿Cuantas letras máximo por trozo? (1000)
        # - chunk_overlap: ¿Cuantas letras repetimos entre trozos para no perder el hilo? (200)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            # Lista de separadores preferidos: Primero intenta por párrafos, luego por frases, etc.
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        
    def load_documents(self) -> List[Document]:
        """Carga documentos markdown del directorio docs y enriquece sus metadatos."""
        print(f"Cargando documentos desde {self.docs_path}")
        
        # DirectoryLoader escanea una carpeta entera buscando patrones (glob)
        # Usamos TextLoader porque los .md son texto plano
        loader = DirectoryLoader(
            str(self.docs_path), # convierte esto a texto (string)
            glob="*.md", # solo quiero archivos .md
            loader_cls=TextLoader, # usa esta clase para abrir cada archivo, en este caso como texto plano
            loader_kwargs={"encoding": "utf-8"}
        )
        
        documents = loader.load()

        # un documento dentro de la lista de documentos tienes este aspecto:
        # Document(
        #     page_content='...texto del archivo...\n\n', 
        #     metadata={
        #         'source': '...ruta del archivo...\n\n'}
        # )
        
        # Enriquecimiento de metadatos: fundamental para que la IA tenga contexto
        for doc in documents:
            filename = Path(doc.metadata["source"]).stem # .stem elimina la extension del archivo
            doc.metadata.update({
                "filename": filename, # nombre del archivo sin extension
                "doc_type": self._get_doc_type(filename),
                # Generamos un ID único basado en el contenido
                "doc_id": self._generate_doc_id(doc.page_content)
            })
        
        print(f"Cargados {len(documents)} documentos")
        return documents
    
    def _get_doc_type(self, filename: str) -> str:
        """
        Función auxiliar: Analiza el nombre del archivo para etiquetar el documento.
        Esto permite que la IA sepa si está leyendo una FAQ o un Manual.
        """
        name = filename.lower()
        if "faq" in name:
            return "Preguntas Frecuentes"
        elif "manual" in name:
            return "Manual"
        elif "resolucion" in name or "troubleshooting" in name:
            return "Resolución de Problemas"
        else:
            return "General"
    
    def _generate_doc_id(self, content: str) -> str:
        """Usa una función de hash para crear un ID único por contenido."""
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Paso 2: Cortar los documentos originales en trozos (chunks).
        Esto es vital para no saturar la memoria del modelo y ser más precisos.
        """
        print("Dividiendo documentos en chunks...")
        
        chunks = self.text_splitter.split_documents(documents)
        
        # Guardamos metadatos extras en cada trozo para tener un control total
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                "chunk_id": i,                # ¿Qué trozo de la secuencia es este?
                "chunk_size": len(chunk.page_content) # ¿Cuanto mide exactamente este trozo?
            })
        
        print(f"Creados {len(chunks)} chunks")
        return chunks
    
    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """
        Paso 3: Crear la base de datos de vectores (ChromaDB).
        Aquí es donde el texto se convierte finalmente en números y se guarda en disco.
        """
        print("Creando vectorstore con ChromaDB y Gemini Embeddings...")
        
        # Seguridad: Si ya existe una carpeta de base de datos, la borramos para no mezclar datos viejos.
        if self.chroma_path.exists():
            shutil.rmtree(self.chroma_path)
            print(f"Directorio anterior {self.chroma_path} eliminado")
        
        # Chroma.from_documents hace 3 cosas:
        # 1. Toma los textos
        # 2. Llama a Gemini para vectorizarlos
        # 3. Los guarda en la carpeta 'chroma_db'
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=str(self.chroma_path),
            collection_name="helpdesk_knowledge" 
        )
        
        print(f"Vectorstore creado exitosamente")
        return vectorstore
    
    def load_existing_vectorstore(self) -> Chroma:
        """Carga una base de datos que ya ha sido creada previamente."""
        if not self.chroma_path.exists():
            raise FileNotFoundError(f"Vectorstore no encontrado en {self.chroma_path}")
        
        return Chroma(
            persist_directory=str(self.chroma_path),
            embedding_function=self.embeddings,
            collection_name="helpdesk_knowledge"
        )
    
    def setup_rag_system(self, force_rebuild: bool = False):
        """
        El 'Director de Orquesta': Une todas las funciones anteriores.
        Parametro force_rebuild: Si es True, borra todo y empieza de cero. Si es False, intenta cargar lo que ya hay.
        """
        print("Configurando sistema RAG con Google Gemini...")
        
        # 1. ¿Ya tenemos la base de datos creada?
        if self.chroma_path.exists() and not force_rebuild:
            print("Cargando base de datos vectorial existente...")
            return self.load_existing_vectorstore()
        
        # 2. Si no, ejecutamos toda la tubería (Pipeline) -> Carga -> División -> Vectorización
        documents = self.load_documents()
        if not documents:
            print("No se encontraron documentos en la ruta especificada.")
            return None
            
        chunks = self.split_documents(documents)
        vectorstore = self.create_vectorstore(chunks)
        
        print("Sistema RAG configurado y listo")
        return vectorstore
    
    def test_search(self, vectorstore: Chroma, query: str = "resetear contraseña"):
        """Realiza una búsqueda de prueba para validar el sistema."""
        print(f"\nProbando búsqueda: '{query}'")
        
        # k=3 nos devuelve los 3 fragmentos más similares
        results = vectorstore.similarity_search(query, k=3)
        
        for i, doc in enumerate(results, 1):
            print(f"\nResultado {i}:")
            print(f"Tipo: {doc.metadata.get('doc_type', 'unknown')}")
            print(f"Archivo: {doc.metadata.get('filename', 'unknown')}")
            print(f"Contenido: {doc.page_content[:150]}...")
        
        return results

def main():
    """Función principal de ejecución del script setup_rag.py"""
    print("="*50)
    print("CONFIGURACION SISTEMA RAG - GOOGLE GEMINI")
    print("="*50)
    
    # 1. Instanciamos el procesador
    processor = DocumentProcessor()
    
    # 2. Configuramos el sistema (forzamos rebuild la primera vez)
    vectorstore = processor.setup_rag_system(force_rebuild=False)
    
    if vectorstore:
        # 3. Realizamos búsquedas de validación
        test_queries = [
            "¿Cómo reseteo mi contraseña?",
            "Tengo un error 500",
            "Quiero cancelar mi suscripción"
        ]
        
        for query in test_queries:
            processor.test_search(vectorstore, query)
    
    print("\nProceso de configuración finalizado con éxito.")

if __name__ == "__main__":
    main()
    
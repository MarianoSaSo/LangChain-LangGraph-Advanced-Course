# 🌟 Teoría: Bases de Datos Vectoriales (Vector Stores)

## 🗄️ ¿Qué es una Base de Datos Vectorial?

A medida que avanzamos en la construcción de aplicaciones basadas en Inteligencia Artificial y nos acercamos al concepto de **RAG (Retrieval-Augmented Generation)**, nos encontramos con la necesidad de almacenar información. 

Una base de datos vectorial (o *Vector Store*) es una base de datos **especializada en almacenar vectores numéricos (embeddings)**. A diferencia de las bases de datos relacionales tradicionales (como MySQL) o NoSQL (como MongoDB) que almacenan texto o datos estructurados, estas bases de datos guardan la "huella digital semántica" de la información.

---

## 🔍 Búsqueda por Similitud Semántica (Similarity Search)

La principal diferencia y ventaja de una base de datos vectorial radica en **cómo busca la información**.

- **BBDD Tradicional:** Realiza búsquedas mediante coincidencias exactas (por ejemplo: `WHERE nombre = 'María'`). Si la palabra no coincide carácter por carácter, no devuelve el registro.
- **BBDD Vectorial:** Evalúa la **similitud semántica**. Si buscamos sobre "mascotas pequeñas", podría devolvernos documentos que contengan la palabra "gato" o "perro", aunque "mascotas pequeñas" no aparezca de forma literal en el texto. Esto lo hace calculando matemáticamente las distancias entre vectores (ej. similitud del coseno).

Para aplicaciones de Inteligencia Artificial que tratan de "entender" lo que pregunta el usuario, esta capacidad es fundamental e insustituible.

---

## ⚙️ ¿Cómo funciona el proceso completo?

El flujo de trabajo habitual con las bases de datos vectoriales suele dividirse en dos grandes fases:

### Fase 1: Ingesta (Guardar datos)
1. **Cargar:** Recibimos los documentos (PDFs, webs, txts largos).
2. **Fragmentar (Split):** Cortamos esos documentos largos en trozos lógicos y pequeños (chunks) utilizando herramientas como el `RecursiveCharacterTextSplitter`.
3. **Embeddings:** Transformamos cada *chunk* de texto en un vector numérico usando un modelo de embeddings (como el de Google o el de OpenAI).
4. **Indexar:** Guardamos el texto base y su vector asociado en la Base de Datos Vectorial para un rápido acceso en el futuro.

### Fase 2: Búsqueda (Recuperar datos)
1. **Consulta:** El usuario hace una pregunta en lenguaje natural.
2. **Vectorizar pregunta:** Convertimos esa pregunta a un formato vectorial utilizando **el mismo modelo de embeddings** que en la fase de ingesta.
3. **Comparar:** La base de datos calcula qué vectores almacenados están "físicamente más cerca" en el espacio multidimensional respecto al vector de la consulta.
4. **Retornar:** Devuelve los fragmentos o documentos de texto asociados a los vectores más similares para que la IA disponga de ese contexto.

---

## 🛠️ Herramientas y Opciones en el Mercado

Existen múltiples bases de datos vectoriales. LangChain, con su interfaz unificada, nos permite usar cualquiera de ellas sin apenas cambiar nuestro código:

- **Chroma (ChromaDB):** Es una base de datos *Open Source*, gratis y pensada para uso local. Muy popular para aprender, iterar prototipos rápidamente y pequeños proyectos. Es la que utilizamos en nuestras prácticas iniciales.
- **Pinecone:** Orientada a producción y proyectos a escala comercial. Es completamente gestionada en la nube ("Serverless"), lo cual elimina la carga de mantenimiento, pero conlleva un coste asociado a gran escala.
- **Qdrant / Milvus / Weaviate:** Otras alternativas súper potentes y muy comunes en el ecosistema, con variaciones en sus algoritmos de indexación en formato híbrido u open-source.

Independientemente de la que se elija, gracias a LangChain los métodos `.from_documents()` o `.similarity_search()` funcionan de una forma casi idéntica, blindando nuestro código ante futuros cambios tecnológicos.




CODIGO DE LA LECCION 

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFDirectoryLoader("C:\\Users\\santiago\\curso_langchain\\Tema 3\\contratos")
documentos = loader.load()

print(f"Se cargaron {len(documentos)} documentos desde el directorio.")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=5000,
    chunk_overlap=1000
)

docs_split = text_splitter.split_documents(documentos)

print(f"Se crearon {len(docs_split)} chunks de texto.")

vectorstore = Chroma.from_documents(
    docs_split,
    embedding=OpenAIEmbeddings(model="text-embedding-3-large"),
    persist_directory="C:\\Users\\santiago\\curso_langchain\\Tema 3\\chroma_db"
)

consulta = "¿Dónde se encuentra el local del contrato en el que participa María Jiménez Campos"

resultados = vectorstore.similarity_search(consulta, k=2)

print("Top 3 documentos mas similares a la consulta:\n")
for i, doc in enumerate(resultados, start=1):
    print(f"Contenido: {doc.page_content}")
    print(f"Metadatos: {doc.metadata}")

# 🎓 Master Class: Configuración del Sistema RAG (Helpdesk 2.0)

Bienvenidos a la guía teórica definitiva sobre cómo construir la base de un sistema de Inteligencia Artificial que "lee" y "entiende" documentos privados. En esta lección aprendemos a configurar el **RAG (Retrieval Augmented Generation)** usando **Google Gemini** y **ChromaDB**.

---

## 1. ¿Qué es RAG y por qué lo necesitamos?

Normalmente, un modelo como Gemini sabe mucho sobre el mundo, pero **no sabe nada sobre tu empresa**. Si le preguntas "¿Cómo reseteo la clave en la App de Helpdesk de mi oficina?", el modelo alucinará o dirá que no sabe.

El **RAG** soluciona esto en 3 pasos:
1.  **Recuperación (Retrieval):** Busca en tus documentos (.md, .pdf) la información relevante.
2.  **Aumentación (Augmented):** Añade esa información a la pregunta del usuario.
3.  **Generación (Generation):** Gemini responde usando esos datos "frescos".

---

## 2. El Pipeline de Procesamiento (Paso a Paso)

Para que la IA pueda buscar en nuestros documentos, primero debemos transformarlos. Este es el flujo que implementamos en `setup_rag.py`:

### Paso A: Carga de Documentos (`DirectoryLoader`)
No abrimos los archivos uno a uno. Usamos herramientas que escanean carpetas enteras.

```python
# Ejemplo de carga de archivos Markdown
loader = DirectoryLoader("./docs", glob="*.md", loader_cls=TextLoader)
documents = loader.load()
```

### Paso B: División Inteligente (`Text Splitting`)
Los documentos largos son difíciles de procesar. Los cortamos en **Chunks** (fragmentos).
- **Chunk Size (1000):** El tamaño ideal para que quepa en la memoria del modelo.
- **Chunk Overlap (200):** Repetimos el final de un fragmento al principio del siguiente para no cortar frases por la mitad y perder el sentido.

```python
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)
```

### Paso C: Vectorización (`Embeddings`)
Aquí ocurre la magia. Gemini convierte el texto en una lista de miles de números llamada **Vector**. 
> Si dos frases tienen significados similares, sus vectores estarán "cerca" matemáticamente.

### Paso D: Almacenamiento (`Vector Store`)
Guardamos esos vectores en **ChromaDB**. Es como una biblioteca donde los libros no se ordenan por título, sino por **significado**.

---

## 3. La Importancia de los Metadatos

En nuestro proyecto, enriquecemos cada trozo de texto con información extra:
- `doc_type`: ¿Es un manual o una FAQ?
- `source`: ¿De qué archivo vino?
- `chunk_id`: ¿Qué posición ocupa?

**¿Para qué sirve?** Para que cuando Gemini nos dé una respuesta, podamos decirle al usuario: *"Esta información la he sacado de la página 5 del Manual de Usuario"*. ¡Esto genera confianza!

---

## 4. Conceptos Clave para el Examen / Proyecto

| Concepto | Explicación Simple |
| :--- | :--- |
| **Embeddings** | La "traducción" de palabras a números que la IA entiende. |
| **ChromaDB** | La base de datos que guarda esos números y permite buscar por significado. |
| **Similarity Search** | Buscar lo más "parecido" a la pregunta del usuario, no solo palabras exactas. |
| **Stemming / Path** | Limpiar los nombres de archivos (ej: de `manual.md` a `manual`) para que los metadatos sean legibles. |

---

## 5. El "Director de Orquesta": `setup_rag_system`

En nuestro código, hemos creado un método que decide si debe trabajar o no:
1.  Si la base de datos ya existe, **la carga** (ahorramos tiempo y dinero).
2.  Si activamos `force_rebuild=True`, **borra todo y reconstruye**. 

Esto es una **buena práctica profesional**: no queremos gastar recursos de API cada vez que reiniciamos nuestra aplicación.

---

> [!TIP]
> **Consejo para Estudiantes:** Intentad cambiar el `chunk_size` en el archivo `config.py` y observad cómo cambia la precisión de las respuestas. ¡La experimentación es la clave del aprendizaje en IA!

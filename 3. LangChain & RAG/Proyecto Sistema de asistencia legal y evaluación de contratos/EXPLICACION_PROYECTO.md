# ⚖️ Guía Maestra: Sistema de Asistencia Legal y Evaluación de Contratos (RAG)

## 📖 Introducción al Proyecto
Este es el proyecto capstone del **Módulo 3: LangChain & RAG**. No es una simple aplicación que "lee PDFs"; es un sistema de grado profesional diseñado para resolver problemas reales en el sector legal. A lo largo de esta guía, desglosaremos cada decisión técnica y arquitectónica basada en las clases impartidas.

---

## 🏗️ PARTE 1: La Fuente de Conocimiento Externa (Indexación)
*Concepto clave: El almacén de vectores como cimiento.*

Cuando diseñamos una aplicación RAG, lo primero que identificamos es la **fuente de conocimiento externa**. En nuestro caso, son contratos de arrendamiento complejos (viviendas, locales comerciales, plazas de garaje).

### 1.1 La Base de Datos: ChromaDB
Utilizamos **ChromaDB** por su eficiencia y capacidad de realizar búsquedas semánticas. Tal como explicamos en la lección 1 del proyecto, los resultados óptimos en RAG dependen de cómo se almacena la información inicial.

### 1.2 Estrategia de División de Texto (Text Splitting)
Aquí tomamos una decisión fundamental. En lecciones anteriores usamos `chunk_size` de 1000, pero para contratos legales hemos subido a **5000 caracteres con un overlap de 1000**.
- **¿Por qué 5000?** Los fragmentos pequeños pierden información contextual. Si una cláusula de duración está separada del nombre de las partes, la IA no podrá relacionarlas. 5000 nos permite capturar secciones completas del contrato en un solo bloque.
- **¿Por qué 1000 de superposición?** Para asegurar que la transición entre fragmentos sea suave y no se corte una sentencia crítica por la mitad.

### 1.3 El Script `vector_store.py`
Este script realiza el proceso de "Ingestión":
1. Lee los PDFs del directorio `/contratos`.
2. Aplica el `RecursiveCharacterTextSplitter`.
3. Genera Embeddings con `models/gemini-embedding-001`.
4. Almacena y persiste los datos en la carpeta `/chroma_db`.

---

## ⚙️ PARTE 2: Arquitectura Modular y Profesionalización
*Concepto clave: Separar configuración de lógica.*

Un sistema robusto no tiene "hardcoded" los nombres de los modelos o las rutas. Por eso creamos **`config.py`**.

### 2.1 La Estrategia de "Doble Modelo"
Una de las técnicas más avanzadas que aprendimos es usar dos LLMs distintos:
- **Query Model (`QUERY_MODEL`)**: Se encarga de la reformulación de consultas (MultiQuery). Este modelo suele ser rápido.
- **Generation Model (`GENERATION_MODEL`)**: Se encarga de leer el contexto legal y escribir la respuesta final. Aquí buscamos la máxima precisión.

### 2.2 Variables Globales
En `config.py` definimos también los parámetros del Retriever (K=2, Lambda=0.7, Fetch_K=20), permitiendo que cualquier ajuste fino (fine-tuning) se haga desde un solo lugar sin tocar el código del sistema.

---

## 🔍 PARTE 3: Estrategias de Recuperación Avanzada
*Concepto clave: MMR y Multi-Query.*

### 3.1 MMR (Maximal Margin Relevance) vs Similitud de Coseno
La similitud de coseno estándar puede devolvernos fragmentos casi idénticos (duplicados). El **MMR** es superior para nosotros porque busca un equilibrio entre:
1. **Relevancia**: Que el fragmento responda a la pregunta.
2. **Diversidad**: Que los fragmentos recuperados sean distintos entre sí para cubrir más partes del contrato.
Usamos un `lambda_mult` de **0.7** para priorizar la relevancia pero sin sacrificar la diversidad.

### 3.2 Personalización del MultiQueryRetriever
No dejamos que LangChain use su prompt por defecto. En **`prompts.py`** definimos el `MULTI_QUERY_PROMPT`.
Le decimos a la IA: *"Eres un experto legal... genera variaciones considerando sinónimos técnicos"*. Esto permite que si el usuario pregunta por "alquiler", la IA también busque por "renta", "arrendamiento" o "contraprestación".

### 3.3 El Ensemble (Búsqueda Híbrida)
Combinamos lo mejor de dos mundos en el `EnsembleRetriever`:
- **70% de peso a MMR + MultiQuery**.
- **30% de peso a Similarity pura**.
Esto garantiza que nunca perdamos el fragmento más relevante, pero que siempre tengamos contexto variado.

---

## 🧠 PARTE 4: La Cadena RAG y el Lenguaje LCEL
*Concepto clave: Conectar componentes con el operador Pipe (`|`).*

En `rag_system.py`, construimos la arquitectura final. Es una interconexión compleja que resuelve el 99% de los casos de uso empresariales.

```python
rag_chain = (
    {
        "context": final_retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm_generation
    | StrOutputParser()
)
```

### El Uso de `RunnablePassthrough`
Esta clase actúa como un "placeholder". Le decimos a la cadena: *"Todavía no sé qué preguntará el usuario, así que cuando llegue la pregunta ('question'), pásala directamente adelante sin modificarla"*.

---

## 🛠️ PARTE 5: Resolviendo el "Problema de Desconexión"
*Concepto clave: La función `format_docs`.*

Este es probablemente el paso más importante que aprendimos en el curso. 

### El Problema
Si recuperamos un fragmento sobre "duración" y otro sobre "nombres de partes", están desconectados. La IA no sabe si pertenecen al mismo contrato.

### La Solución Técnica
En la función `format_docs`, preprocesamos cada fragmento antes de inyectarlo al prompt:
1. Extraemos de los metadatos la **Fuente (Source)** y la **Página**.
2. Creamos una cabecera para cada fragmento: `[Fragmento 1] - Fuente: Contrato_A.pdf - Página: 5`.
3. Concatenamos esta cabecera con el contenido.

**Resultado:** Al recibir el contexto, el LLM lee: 
*"En el fragmento 1 (que es del Contrato B en página 2) dice que el inquilino es Juan, y en el fragmento 2 (que también es del Contrato B en página 4) dice que la fianza es de 1000€"*. 
**¡Ahora la IA puede relacionar fragmentos y dar respuestas precisas sin alucinar!**

---

## 💻 PARTE 6: La aplicación en Producción (Streamlit)
*Concepto clave: Cache y Experiencia de Usuario.*

### 6.1 Eficiencia con `@st.cache_resource`
No queremos que Streamlit recree la base de datos o instancie los modelos cada vez que enviamos un mensaje. El decorador `cache_resource` almacena el sistema RAG en la memoria rápida, haciendo que la respuesta sea casi instantánea tras la primera carga.

### 6.2 Visualización de Evidencias
Tal como mostramos en la `app.py`, no solo mostramos la respuesta. En la columna derecha de la interfaz, desplegamos los **fragmentos originales** usados. Esto da confianza al usuario legal, permitiéndole verificar lo que dice la IA.

---

## 🚀 Guía de Puesta en Marcha

1. **Instalar Dependencias**: Asegúrate de tener `langchain`, `langchain-google-genai`, `chromadb` y `streamlit`.
2. **Generar la BD**: Ejecuta `python vector_store.py`. Verás que se generan los 15 fragmentos iniciales.
3. **Lanzar la APP**: `streamlit run app.py`.

### 💡 Tarea para el Alumno
Observa los archivos `RELEVANCE_PROMPT` y `ENTITY_EXTRACTION_PROMPT` en `prompts.py`. No los estamos usando en la cadena base. **Reto:** Intenta integrarlos en la función `format_docs` para que la IA filtre los documentos irrelevantes antes de pasarlos al prompt final. ¡Esto elevará tu sistema al siguiente nivel!

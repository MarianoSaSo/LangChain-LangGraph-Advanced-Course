# 🔍 Teoría: Retrievers en LangChain

## 🏹 ¿Qué es un Retriever?

El **Retriever** es el componente final del proceso de gestión de información externa en una aplicación de IA. 

Hasta ahora hemos visto:
1. **Document Loaders:** Cargar información.
2. **Text Splitters:** Dividir y procesar documentos en fragmentos (chunks).
3. **Bases de Datos Vectoriales:** Almacenar vectores semánticos (Embeddings).

El **Retriever** es una abstracción que se encarga de que, dada una consulta (query), busque y retorne un conjunto de documentos relevantes. En otras palabras, **encapsula la lógica de búsqueda** para que el resto de la aplicación no tenga que preocuparse de cómo se obtienen esos documentos.

---

## 📄 ¿Qué devuelve un Retriever?

Es fundamental entender que los retrievers siempre devuelven objetos de la clase `Document`. Como ya hemos visto en lecciones previas, un objeto `Document` contiene:
- `page_content`: El contenido textual del fragmento.
- `metadata`: Un diccionario con información adicional (nombre del archivo, número de página, etc.).

Al usar esta clase estándar, LangChain asegura que todos sus componentes (como las Chains o los Agentes) puedan trabajar con la información recuperada de forma unificada.

---

## 🛠️ Interfaz Unificada: El método `.invoke()`

A diferencia de las bases de datos vectoriales que tienen métodos específicos como `.similarity_search()`, los retrievers utilizan una **interfaz común**. 

El método principal es `.invoke(consulta)`. 

Esto es una gran ventaja porque:
- **Flexibilidad:** Permite cambiar el sistema de almacenamiento (por ejemplo, de Chroma a Pinecone) sin cambiar el código de recuperación.
- **Estandarización:** Sigue la filosofía de LangChain de usar una interfaz predecible en todo su ecosistema.

---

## ⚙️ Configuración del Retriever

Cuando instanciamos un retriever a partir de una base de datos vectorial mediante `.as_retriever()`, podemos pasarle parámetros clave:

1. **`search_type`:** Define el algoritmo de búsqueda. Por defecto es `similarity` (búsqueda semántica), pero existen otros tipos más avanzados.
2. **`search_kwargs`:** Un diccionario de argumentos adicionales. El más común es `{"k": n}`, donde `n` es el número de fragmentos que queremos recuperar.

---

## 💡 Nota importante: Retrievers vs Loaders

Es común que surja la duda entre estos dos componentes:
- **Document Loaders:** Sirven para **ingestar** datos (fase inicial).
- **Retrievers:** Sirven para **recuperar** datos de un almacén persistente de forma eficiente.

> [!TIP]
> En aplicaciones avanzadas, utilizaremos "Smart Retrievers" (Retrievers Inteligentes) que incorporan lógica adicional para filtrar duplicados o re-rankear los resultados usando modelos de lenguaje.

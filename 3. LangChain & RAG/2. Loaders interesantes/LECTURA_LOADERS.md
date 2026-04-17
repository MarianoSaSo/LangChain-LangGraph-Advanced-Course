# 📖 Lectura: Document Loaders interesantes en LangChain

Los **Document Loaders** son uno de los componentes más versátiles y útiles del ecosistema LangChain. Permiten convertir prácticamente cualquier fuente de información en documentos estructurados que pueden ser procesados por modelos de lenguaje. 

En este artículo exploraremos los loaders más interesantes y útiles, con ejemplos prácticos para cada uno.

---

### 1. WebBaseLoader - El Poder de la Web
Perfecto para extraer contenido de páginas web de forma sencilla.
*   **Ideal para:** Documentación técnica, blogs, noticias.
*   **Librería:** `pip install beautifulsoup4`

### 2. PyPDFLoader - Documentos PDF Inteligentes
Extrae información página por página preservando el número de página en los metadatos.
*   **Ideal para:** Manuales, contratos, papers académicos.
*   **Librería:** `pip install pypdf`

### 3. DirectoryLoader - Procesamiento Masivo
Permite procesar múltiples archivos de una carpeta completa de forma eficiente.
*   **Ideal para:** Bases de conocimiento locales, repositorios de documentación.
*   **Librería:** `pip install unstructured`

### 4. YoutubeLoader - Contenido Multimedia
¡Extrae transcripciones automáticas de videos de YouTube!
*   **Ideal para:** Analizar conferencias, resúmenes de videos educativos.
*   **Librería:** `pip install youtube-transcript-api pytube`

### 5. CSVLoader - Datos Tabulares
Convierte datos estructurados de hojas de cálculo en documentos procesables.
*   **Ideal para:** Logs de sistema, datos de encuestas, reportes de ventas.

### 6. SeleniumURLLoader - JavaScript y Contenido Dinámico
Para páginas web modernas (SPAs) que requieren renderizado de JavaScript antes de leer el contenido.
*   **Librería:** `pip install selenium`

### 7. GitLoader - Repositorios de Código
Carga archivos directamente desde repositorios Git remotos o locales.
*   **Librería:** `pip install GitPython`

---

> [!NOTE]
> Recuerda que cada documento cargado siempre contendrá los dos campos estándar: `page_content` y `metadata`. La riqueza de los metadatos dependerá de qué tan especializado sea el loader que utilices.

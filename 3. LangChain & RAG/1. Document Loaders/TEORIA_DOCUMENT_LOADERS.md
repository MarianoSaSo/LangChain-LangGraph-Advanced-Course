# 📚 Tema 3: LangChain & RAG
## Lección 1: Document Loaders

### ¿Qué son los Document Loaders?
Los **Document Loaders** son componentes de LangChain (ubicados en la librería `langchain-community`) diseñados para importar datos desde fuentes externas y convertirlos a un formato unificado que la IA pueda entender. 

Actúan como "traductores" que toman archivos brutos (PDFs, webs, bases de datos) y los transforman en objetos estándar de LangChain llamados **Documents**.

---

### El Objeto `Document`
Independientemente de si cargas un PDF, una web o un mensaje de Slack, LangChain siempre te devolverá una lista de objetos `Document`. Cada objeto contiene principalmente dos campos:

1.  **`page_content`**: Es una cadena de texto (`string`) que contiene el contenido textual del documento cargado.
2.  **`metadata`**: Un diccionario (`dict`) con información adicional sobre el origen del documento. 
    *   *Ejemplo en PDF:* número de página, nombre del archivo, autor, fecha de creación.
    *   *Ejemplo en Web:* título de la página, descripción, URL.

---

### Tipos de Loaders
Existen más de **1,000 loaders** disponibles. Algunos de los más comunes son:
*   **Archivos Locales:** PDF, CSV, TXT, Microsoft Word, JSON.
*   **Fuentes Online:** Páginas web, YouTube (transcripciones), Wikipedia.
*   **Plataformas en la nube:** Google Drive, Notion, Slack, GitHub, S3.

---

### Dependencias Necesarias
Muchos loaders son integraciones con librerías externas especializadas. Para seguir esta lección, asegúrate de tener instaladas:

```bash
# Para procesar archivos PDF
pip install pypdf

# Para procesar páginas web (extracción estática)
pip install beautifulsoup4
```

---

### Funcionamiento Básico
El flujo de trabajo siempre sigue este patrón:
1.  **Importar** el loader específico.
2.  **Instanciar** el loader con la ruta o URL necesaria.
3.  **Llamar al método `.load()`**, que devuelve la lista de documentos.

> [!TIP]
> En el caso de los PDFs, el método `.load()` suele devolver un objeto `Document` por cada página del archivo, lo que facilita mucho el procesamiento posterior.

# 📄 Sistema de Evaluación de CVs y Candidatos con IA

Este es el proyecto integrador (capstone) del **Módulo 2 (Fundamentos Componentes Core)**. Reúne todos los conceptos clave vistos hasta la fecha aplicados sobre un caso de uso real: analizar textos no estructurados (currículums en PDF) y convertirlos en evaluaciones objetivas, útiles para áreas de Recursos Humanos o candidatos.

---

## 🏗️ Arquitectura del Proyecto

El proyecto está diseñado de forma modular. Esta es la mejor práctica en la creación de aplicaciones con LLMs, separando la lógica de Inteligencia Artificial (modelos y prompts) de la lógica de procesamiento (PDFs) y la interfaz visual.

### 1. Modelos (Pydantic)
*Archivo: `models/cv_model.py`*

Aquí definimos la estructura perfecta de datos (JSON) que queremos que la Inteligencia Artificial nos devuelva. Heredamos de la clase `BaseModel` de **Pydantic**.
Esta es una evolución directa del "Experimento Pokémon" (Tarea 2). El LLM leerá nuestro esquema y convertirá las respuestas abiertas ("el candidato tiene experiencia en esto y aquello...") en un objeto JSON predecible.

- **Componente clave:** `Field(description="...")`. Las descripciones dentro de cada "Field" son en realidad mini-prompts estructurados. El LLM se guía por estos textos para saber qué valor rellenar (por ejemplo, qué porcentaje de ajuste darle o cuántos años de experiencia inferir).

### 2. Prompts (Plantillas Compuestas)
*Archivo: `prompts/cv_prompts.py`*

A diferencia de la introducción, aquí construimos un Prompt compuesto avanzado usando `ChatPromptTemplate` desde LangChain.
- **`SystemMessagePromptTemplate`**: Define el rol ("experto reclutador senior") y le da los parámetros de comportamiento, evaluación y severidad.
- **`HumanMessagePromptTemplate`**: Es la capa abierta donde inyectamos dinámicamente las variables de negocio (`{texto_cv}` y `{descripcion_puesto}`).

### 3. Evaluador Core (LCEL y Structured Output)
*Archivo: `services/cv_evaluator.py`*

Este es el cerebro del sistema que une el modelo generativo (OpenAI) con nuestra estructura (Pydantic) y los Prompts.
-  **El Método Moderno:** Utiliza `modelo_base.with_structured_output(AnalisisCV)`. Esta función le "ata las manos" al LLM de OpenAI: ya no le permite generar un párrafo de texto libre, sino que lo obliga por protocolo a devolver un objeto final de clase `AnalisisCV`.
-  **LCEL (Cadena de LangChain):** Se forma conectando el prompt con el modelo estructurado en la sintaxis de "pipelines": `cadena_evaluacion = chat_prompt | modelo_estructurado`.

### 4. Procesador de Archivos PDF
*Archivo: `services/pdf_processor.py`*

No es IA, pero es vital. El LLM no puede "ver" el archivo binario, solo procesa texto. Usamos la biblioteca `PyPDF2` genérica de Python para desempaquetar las páginas de los PDFs subidos en la interfaz y sacar todo el contenido crudo (RAW) y pasárselo a la IA en el Human Message.

### 5. Interfaz de Usuario Visual (Streamlit)
*Archivos: `ui/streamlit_ui.py` y `main.py`*

Construimos un panel dividido en dos columnas:
- **Columna Izquierda (Entrada):** Permite subir archivos y escribir un *Job Description* usando la librería `streamlit`.
- **Columna Derecha (Salida):** Muestra los datos mapeados directamente desde nuestro objeto Pydantic (`resultado.fortalezas`, `resultado.porcentaje_ajuste`, etc.). No tenemos que parsear texto, solo imprimir la variable, porque Pydantic ya hizo todo el trabajo por nosotros.

---

## 💡 Lecciones Claves para Estudiantes (Para remarcar en tu video)

1. **"Basura entra -> Basura sale" (GIGO):** El código funciona excelente, sin embargo, el análisis será bueno únicamente si el **currículum es rico en texto** y el área de **descripción del puesto de trabajo es muy detallada**. Esto remarca la importancia de un buen contexto en los LLM.
2. **Dependencias:** Este proyecto usa `PyPDF2`, no instalada por defecto. Siempre hay que hacer `pip install PyPDF2` cuando sumamos bibliotecas nuevas de pre-procesamiento de datos.
3. **Flujo de Ejecución:** Para ejecutar este software no se hace con el plugin de "Play" de Python (como el error de `main.py`), sino invocando el servidor interno de Streamlit con el comando en consola: `streamlit run main.py`.

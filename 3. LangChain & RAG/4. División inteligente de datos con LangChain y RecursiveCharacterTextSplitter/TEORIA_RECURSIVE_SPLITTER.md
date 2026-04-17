# ✂️ RecursiveCharacterTextSplitter: División Inteligente de Datos

En la lección anterior vimos que no podemos enviar un libro o documento completo a un LLM porque superaríamos el límite de nuestra "Ventana de Contexto" (Context Window) y además sería muy ineficiente.

La solución es dividir la información en pequeños trozos o fragmentos (conocidos como **Chunks**).

---

## 🚀 ¿Por qué RecursiveCharacterTextSplitter es el mejor?

Dentro del módulo `langchain_text_splitters`, encontramos distintas estrategias de división matemática. El **RecursiveCharacterTextSplitter** es considerado el estándar de la industria y la opción más inteligente. 

¿Por qué? Porque en lugar de cortar ciegamente cada X número de caracteres (lo que podría romper una palabra o frase a la mitad), **intenta mantener la estructura semántica original**.

Su estrategia de división es recursiva. Empieza buscando el corte más "limpio" y si el fragmento sigue siendo muy grande, va probando opciones más agresivas:
1.  Dobles saltos de línea (párrafos) `\n\n`
2.  Saltos de línea sencillos `\n`
3.  Espacios en blanco `" "`
4.  Caracteres individuales `""`

---

## ⚙️ Parámetros Fundamentales

Al instanciar la clase `RecursiveCharacterTextSplitter`, hay dos argumentos clave:

### 1. `chunk_size` (Tamaño del Fragmento)
Es el número aproximado de caracteres que queremos por cada fragmento. 
**Nota:** El modelo prefiere cortes limpios (como un fin de párrafo) antes que cumplir estrictamente con el número exacto, por eso es un valor aproximado.

### 2. `chunk_overlap` (Solapamiento)
Esta es una técnica vital en Inteligencia Artificial. Cuando creamos un "Chunk 2", le introducimos los últimos caracteres del "Chunk 1". 
*   **¿Para qué sirve?** Evita perder el contexto si el algoritmo cortó el texto a la mitad de una idea compleja. Al leer el segundo fragmento, el LLM tendrá un pequeño "recordatorio" de cómo terminó el anterior.
*   **Recomendación:** Un overlap de entre 100 y 200 caracteres suele funcionar genial en la mayoría de los casos.

---

## 🗂️ split_documents vs split_text

*   **`split_text(texto)`**: Recibe un String (cadena de texto) gigante y devuelve una lista de Strings más pequeños.
*   **`split_documents(pages)`**: Es increíblemente potente y el que más usarás. Recibe directamente la lista resultante de nuestro cargador (ej: `PyPDFLoader`) y devuelve una nueva lista de objetos "Document". **Mantiene toda la metadata intacta** (la página de la que venía el texto original, autor, etc.).

---

## 🧠 Flujo de Resumen Iterativo (Map-Reduce Básico)

El ejercicio práctico de esta lección implementa una estrategia fundamental de resumen para documentos largos:

1.  **Iterar los Chunks:** Recorremos con un bucle `for` cada fragmento del documento original.
2.  **Resumen Parcial (Map):** Invocamos a nuestro LLM (`gpt-4o-mini`) pidiendo que resuma únicamente ese fragmento, y lo guardamos en una lista.
3.  **Resumen Final (Reduce):** Juntamos todos los resúmenes parciales (con `str.join()`) en un único gran bloque de texto, y le pedimos al LLM que construya un un resumen coherente y completo sobre esas ideas principales.

> [!WARNING]
> Cuidado con los costes de la API. En el ejercicio usamos un contador y un condicional `break` a los 10 primeros fragmentos. Si corres este script sobre todos los fragmentos del Quijote sin detenerlo, realizarás cientas de peticiones sucesivas al LLM y podría consumir bastante crédito de tu cuenta de OpenAI.

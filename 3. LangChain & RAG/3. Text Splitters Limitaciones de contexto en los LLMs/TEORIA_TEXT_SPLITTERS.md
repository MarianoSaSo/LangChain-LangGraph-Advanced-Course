# ✂️ Text Splitters: Superando las Limitaciones de los LLMs

En esta lección aprenderemos uno de los componentes más críticos de **LangChain** cuando trabajamos con grandes volúmenes de información (como PDFs largos, bases de datos o documentación técnica).

---

## 🛑 El Problema: El "Context Window" (Ventana de Contexto)

Todos los modelos de lenguaje (GPT-4o, Gemini, Claude) tienen un límite físico de información que pueden procesar en una sola interacción. Este límite se mide en **Tokens**.

### 1. ¿Qué es un Token?
*   No es exactamente una palabra.
*   **Equivalencia aproximada:** 100 tokens ≈ 75 palabras.
*   Modelos como `gpt-4o-mini` tienen una ventana de hasta **128,000 tokens**. 

### 2. ¿Por qué falla el sistema con documentos grandes?
Cuando intentamos enviar un libro entero (como el Quijote) directamente en el prompt:
1.  **Error 429 (Too many tokens):** El modelo rechaza la petición porque supera su capacidad física.
2.  **Pérdida de Atención:** Incluso si el modelo lo aceptara, los LLMs tienden a "perderse" o ignorar información importante que está en el medio del texto (**Lost in the Middle**).
3.  **Coste Elevado:** Procesar miles de tokens innecesarios encarece la aplicación.

---

## 🏗️ La Solución: Text Splitters

Un **Text Splitter** es un componente de LangChain que divide el texto largo en fragmentos más pequeños y manejables llamados **"Chunks"**.

### ¿Cómo funciona un Splitter?
1.  **Divide el texto** en pequeños trozos (ej: cada 1000 caracteres).
2.  **Crea un solapamiento (Overlap):** Mantiene un poco de texto del final de un fragmento en el inicio del siguiente para no perder el contexto semántico (ej: no cortar una oración a la mitad sin sentido).
3.  **Crea objetos Document:** Convierte cada trozo en un objeto que podemos guardar en una base de datos vectorial.

---

## 🛠️ Tipos de Splitters más comunes

### 1. CharacterTextSplitter
Divide el texto basándose en un carácter específico (por ejemplo, un salto de línea `\n`). Es muy rígido y puede cortar oraciones a la mitad.

### 2. RecursiveCharacterTextSplitter (El Recomendado ⭐)
Es el más inteligente y el que usaremos habitualmente. Intenta mantener los párrafos y oraciones juntos. Su lógica de división es recursiva:
1.  Prueba a dividir por párrafos (`\n\n`).
2.  Si el trozo sigue siendo muy grande, prueba por líneas (`\n`).
3.  Si sigue siendo grande, prueba por espacios (` `).
4.  Finalmente, por caracteres individuales.

---

## ⚙️ Parámetros Clave

*   **`chunk_size`**: El tamaño máximo de cada fragmento (en caracteres o tokens).
*   **`chunk_overlap`**: Cuántos caracteres se repiten entre fragmentos. Recomendado: 10-20% del `chunk_size`.
*   **`length_function`**: La función para medir la longitud (normalmente `len` para caracteres).

---

> [!TIP]
> **Regla de oro:** No existe un `chunk_size` perfecto. Depende de tu caso de uso. Si buscas mucha precisión, usa trozos pequeños. Si buscas contexto general, usa trozos más grandes.

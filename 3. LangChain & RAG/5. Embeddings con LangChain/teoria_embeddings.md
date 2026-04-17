# 🌟 Teoría: Introducción a los Embeddings

## 🧠 ¿Qué es un Embedding?

En el ecosistema de la Inteligencia Artificial moderna y en frameworks como LangChain, los **embeddings** son probablemente una de las técnicas más importantes y son la piedra angular de la **recuperación semántica** y los sistemas RAG (Retrieval-Augmented Generation). 

En términos sencillos:
> Un embedding es una **representación numérica** (un vector matemático o lista de números) que captura el **significado semántico** puro de un fragmento de texto.

Los modelos encargados de generar embeddings reciben un texto en lenguaje natural y lo transforman en un vector de un tamaño fijo predeterminado. Este vector actúa como una especie de **"huella digital semántica"** del texto, representando sus ideas y matices de forma que las máquinas lo entiendan.

---

## 📏 El Espacio Vectorial y la Similitud

La idea fundamental detrás de los embeddings se basa en la forma en que ubicamos estos "vectores" dentro de un espacio matemático multidimensional continuo:

- ✅ **Alta Similitud:** Textos que tengan significados similares producirán vectores que "apuntan" al mismo sitio y estarán **muy cercanos** entre sí en este espacio vectorial.
- ❌ **Baja Similitud:** Textos sobre temas opuestos o significados radicalmente diferentes crearán vectores que estarán **muy alejados** el uno del otro en este espacio.

### 💡 El Ejemplo de París

Imagina que tenemos estas dos frases:
1. *"La capital de Francia es París."*
2. *"París es la ciudad capital de Francia."*

Aunque utilizan un orden distinto y puede variar alguna palabra, semánticamente dicen exactamente lo mismo. Un buen modelo de embeddings procesará el texto, entenderá el significado de fondo y generará dos vectores que estén prácticamente pegados. 

Por el contrario, si evaluamos una tercera frase:
3. *"París es un nombre común para mascotas."*

A primera vista, hay cierto parecido visual ya que incluye la palabra clave *"París"*. Un buscador antiguo por palabras clave podría confundirse. Sin embargo, bajo una "comprensión semántica" proporcionada por un LLM, este significado no tiene nada que ver con hablar de la capital francesa. El vector generado para esta última frase terminará **muy lejos** de los dos primeros.

---

## 🔢 Las Dimensiones del Vector

Cuando pides un embedding para una frase, obtienes de vuelta una larga lista de números. A la longitud de este vector se le conoce como **dimensiones**. 

Cada modelo maneja una complejidad distinta:
- Los modelos base (y usualmente Open Source) manejan alrededor de **768 dimensiones** a **1024 dimensiones**.
- El modelo `text-embedding-004` de Google, frecuentemente arroja vectores de  **768 dimensiones**.
- Los modelos gigantes de otras empresas (como OpenAi y su `text-embedding-3-large`) producen vectores muy refinados de hasta **3072 dimensiones**. 

Cada uno de esos casi mil "números" es una de las "coordenadas" que definen la ubicación del concepto en el gran espacio virtual de entendimiento del modelo. Todos los vectores de un modelo *siempre* devolverán vectores de la misma longitud, sin importar si has introducido una palabra de tres letras o un párrafo de cinco páginas.

---

## 📐 Midiendo la Similitud (La Distancia del Coseno)

Para medir de manera práctica cómo de parecidos son dos vectores, típicamente se aplica la métrica de **Similitud del Coseno** (*Cosine Similarity*). Esta operación matemática calcula al ángulo entre dos vectores asumiendo que parten desde el origen (0,0,0...).

- Si el ángulo es de 0º (van en la misma dirección), su coseno es **1.0**. Esto indica que los textos referencian exactamente lo mismo.
- A medida que se vuelven perpendiculares u opuestos, el valor será más bajo (acercándose a 0 o volviéndose negativo en algunos espacios).

En bases de datos estructuradas por vectores o en aplicaciones RAG con LangChain, este cálculo está optimizado por debajo. Una búsqueda semántica es básicamente nosotros pidiendo *"Calcula las similitudes del coseno y dame los documentos con los valores más cercanos al 1"*.

---

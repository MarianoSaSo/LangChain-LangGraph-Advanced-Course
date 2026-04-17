# Tema 2: Fundamentos y Componentes Core
## Lección 1: Introducción a los Runnables

En esta primera clase del tema vamos a comenzar a profundizar sobre probablemente el concepto más relevante de LangChain: **El concepto de cadena (Chain)**.

Ya habíamos visto en temas anteriores, de manera introductoria, que podíamos crear cadenas en LangChain de diferentes formas:
- A través de clases heredadas (ahora deprecadas).
- A través de la **manera recomendada**: usando el **LangChain Expression Language (LCEL)**.

Si profundizamos un poco sobre la manera en la que se crean estas cadenas usando LCEL, tenemos que hablar de un componente esencial y central dentro de LangChain: **Los Runnables**.

### ¿Qué son los Runnables?
Un **Runnable** es cualquier objeto dentro de LangChain que pueda invocarse. Es decir, cualquier objeto que posea el método `.invoke()` que veíamos, por ejemplo, cuando utilizábamos un LLM.

La función básica de un Runnable es:
1. Recibir una serie de entradas (Inputs).
2. Procesar esa información.
3. Producir una salida (Outputs).

*Ejemplo:* En el caso de un modelo de lenguaje (LLM), este toma un texto de entrada y produce un texto generado de salida.

Lo que realmente están haciendo las cadenas en LangChain, a través de LCEL, es permitirnos **combinar todos estos Runnables** de forma secuencial usando un operador especial: la barra vertical o *pipe* (`|`).

---

### Integrando Código Personalizado: `RunnableLambda`

Algo fundamental de LCEL es que no solamente podemos combinar objetos nativos de LangChain (como LLMs o Prompts), sino que también podemos **convertir funciones personalizadas** que nosotros creemos en Python en objetos Runnable.

Para ello, utilizamos la clase `RunnableLambda` importada desde `langchain_core.runnables`.

#### Ejemplo Práctico: Combinando Funciones Propias en una Cadena

Vamos a crear un script llamado `ejemplo_runnables.py` donde convertiremos dos funciones de Python en objetos Runnable y las conectaremos a través de una cadena.

```python
from langchain_core.runnables import RunnableLambda

# ==========================================
# Paso 1: Usando una Expresión Lambda
# ==========================================
# Las expresiones lambda son funciones anónimas y de una sola línea en Python.
# Aquí recibimos un valor 'x' (por ejemplo, un número) y devolvemos un string.
paso_uno = RunnableLambda(lambda x: f"Numero {x}")

# ==========================================
# Paso 2: Usando una Función Tradicional
# ==========================================
# Definimos una función que duplica un texto y lo devuelve dentro de una lista.
def duplicar_texto(texto):
    return [texto] * 2

# Convertimos nuestra función personalizada en un objeto Runnable
paso_dos = RunnableLambda(duplicar_texto)

# ==========================================
# Creando e Invocando la Cadena con LCEL
# ==========================================
# Usamos el operador "pipe" (|) para ensamblar la cadena secuencialmente
cadena = paso_uno | paso_dos

# Invocamos la cadena utilizando el método estándar .invoke()
# Le pasamos el argumento inicial para la primera función
resultado = cadena.invoke(43)

print(resultado)
```

#### Explicación del Código:
1. **Paso 1:** Al invocar la cadena con el número `43`, la función interna de `paso_uno` procesa este número devolviendo la cadena de texto `"Numero 43"`.
2. **Paso 2:** La salida resultante del *Paso 1* pasa de forma automática a la entrada de `paso_dos`. Esta segunda función duplica el texto recibido y lo convierte en una lista: `["Numero 43", "Numero 43"]`.

Esta es la verdadera magia de las abstracciones Runnable dentro de LangChain: la capacidad de empalmar distintos procesos como si fuesen bloques de Lego.

---

### ¿Qué Sigue?
Hasta aquí hemos visto cómo funciona el procesamiento secuencial básico. Sin embargo, los Runnables no se limitan solo a esto. También nos permiten trabajar con **procesamiento en paralelo** y **procesamiento por lotes (batch)**, lo cual nos abrirá las puertas para optimizar nuestras cadenas de manera masiva. ¡Lo veremos mediante un mini-proyecto en la siguiente clase!

# Tema 2: Fundamentos y Componentes Core
## Lección 3: Procesamiento en Paralelo con RunnableParallel

En la lección anterior vimos cómo resolver el caso práctico del análisis de sentimientos de manera *secuencial*. Si recapacitas sobre esa solución, teníamos una función coordinadora grande (`process_one`) que llamaba primero a la generación del resumen y, una vez que terminaba, llamaba al análisis de sentimientos. 

**¿Es esta la manera más óptima?** No necesariamente.

LangChain optimiza muchísimo todo lo que tiene que ver con la ejecución, y uno de sus mecanismos más importantes para ganar tiempo y eficiencia es el **procesamiento en paralelo**. Para implementarlo, utilizamos un tipo especial de Runnable llamado `RunnableParallel`.

### ¿Qué es el Procesamiento en Paralelo?
El procesamiento en paralelo nos permite ejecutar múltiples operaciones **simultáneamente** sobre el mismo input (la misma entrada de datos).

En nuestro caso práctico, si nos fijamos, las operaciones:
1. Generar el resumen
2. Analizar el sentimiento

**Son completamente independientes.** Ninguna de ellas necesita el resultado de la otra para funcionar. Las dos toman exactamente el mismo input: el texto ya preprocesado. Por lo tanto, no tenemos por qué esperar a que se genere el resumen para empezar a analizar el sentimiento; ¡podemos mandar ambas peticiones al modelo (LLM) al mismo tiempo!

### Refactorización: Transformando Tareas en Ramas (Branches)

Para paralelizarlas, el primer paso es que **cada proceso independiente debe ser su propio Runnable**. 
Convertiremos cada función en una "rama" (branch) del flujo utilizando `RunnableLambda`.

```python
from langchain_core.runnables import RunnableLambda

# Rama 1: Resumen
summary_branch = RunnableLambda(generate_summary)

# Rama 2: Sentimiento
sentiment_branch = RunnableLambda(analyze_sentiment)
```

También necesitamos convertir nuestra función encargada de agrupar los resultados finales (`merge_results`) en un objeto Runnable, ya que ahora formará parte directa del ensamblado con LCEL:
```python
merger = RunnableLambda(merge_results)
```

### El Poder de `RunnableParallel`

Una vez que cada acción es un objeto Runnable, podemos agrupar las acciones simultáneas usando `RunnableParallel`. Esta clase recibe un diccionario de Python. 

- Las **claves** del diccionario indican cómo queremos llamar a los resultados.
- Los **valores** del diccionario son los distintos Runnables que queremos lanzar en paralelo.

```python
from langchain_core.runnables import RunnableParallel

parallel_analysis = RunnableParallel({
    "resumen": summary_branch,
    "sentimiento_data": sentiment_branch
})
```

Al decirle esto a la cadena, LangChain va a orquestar por detrás (gracias a LCEL) que cuando entren los datos a este paso, se dividan y **se procesen al mismo tiempo**. El resultado final de este paso `parallel_analysis` será un diccionario que contendrá los resultados obtenidos de ambas ramas.

### Nuestra Cadena Final LCEL Paralelizada

Ahora, nuestra gran cadena coordinadora con el "pipe" (`|`) es muchísimo más elegante, modular y rápida:

```python
chain = preprocessor | parallel_analysis | merger
```

**Flujo de ejecución interno:**
1. El texto original entra a `preprocessor` y se limpia.
2. El input limpio pasa a `parallel_analysis`.
3. `parallel_analysis` manda el input limpio a `summary_branch` y `sentiment_branch` de forma **simultánea**.
4. Ambos terminan (cuando el más lento responde) y LangChain crea un diccionario con `"resumen"` y `"sentimiento_data"`.
5. Ese diccionario pasa finalmente al nodo `merger`, quien se encarga de formatear la salida final unificada.

### ¿Qué Sigue?
Acabamos de optimizar drásticamente el proceso de un único texto lanzando llamadas paralelizadas al LLM. Pero, ¿Qué ocurre si yo tengo **varias reseñas al mismo tiempo**? ¿Tengo que procesar cada una de las reseñas mediante un bucle `for`, una detrás de otra?

La respuesta es que **no**. ¡Lo resolveremos en el siguiente concepto clave de procesamiento!

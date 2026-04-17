# Estado Avanzado en LangGraph: Annotated Types y Reducers

En esta lección vamos a profundizar en cómo gestionar estados más complejos en LangGraph. Hasta ahora, habéis visto flujos secuenciales donde cada nodo realizaba una tarea y pasaba el resultado al siguiente. Pero, ¿qué sucede cuando varios nodos quieren escribir en la misma "cajita" o clave de nuestro estado?

## 1. El Problema de la Sobrescritura por Defecto

Cuando trabajamos con LangGraph, es muy común encontrarnos con la siguiente casuística: varios nodos producen resultados para una misma clave del estado general.

**Por defecto, LangGraph tiene un comportamiento de "reemplazo"**: 
Si el Nodo A escribe en `acta_reunión` y más adelante el Nodo B vuelve a escribir en `acta_reunión`, la actualización más reciente (la del Nodo B) sobrescribirá por completo el valor anterior. El valor del Nodo A se perderá.

Sin embargo, en procesos reales y complejos, lo que solemos querer es **combinar o acumular** los resultados de múltiples nodos en lugar de reemplazarlos.

---

## 2. La Solución: Annotated Types y Reducers

Para solucionar esto sin tener que gestionar manualmente la acumulación en cada nodo, LangGraph nos proporciona los **Annotated Types** y las funciones **Reducer** (reductoras).

### ¿Qué es una función Reductora?
Es una función básica que:
1. Toma el **valor existente** en una clave del estado.
2. Toma el **nuevo valor** que aporta un nodo.
3. Produce un **valor combinado** (sumando, concatenando, haciendo un merge, etc.).

LangGraph permite usar funciones que ya existen en Python o crear nuestras propias funciones personalizadas.

---

## 3. Implementación Práctica: Registro de Logs

Un caso de uso muy frecuente es querer dejar un registro de **trazas o logs** de cada paso ejecutado para poder auditar el workflow al final.

### Paso 1: Importaciones necesarias
Para usar anotaciones y funciones reductoras, necesitamos importar `Annotated` de la librería `typing` y, comúnmente, la función `add` del módulo `operator`.

```python
from typing import Annotated, TypedDict, List
from operator import add
```

### Paso 2: Definir el Estado con Annotated
En lugar de definir una clave como una simple lista, la envolvemos en `Annotated` para indicarle a LangGraph cómo debe comportarse cuando reciba nuevas actualizaciones.

```python
class State(TypedDict):
    # Definimos 'logs' como una lista de strings que usa 'add' como reductor
    logs: Annotated[List[str], add]
    # ... otras claves (notes, participants, etc.)
```

> [!TIP]
> **¿Qué hace `add` aquí?**
> * Si el tipo es `List`, `add` significa **concatenar** las listas.
> * Si el tipo fuera `int`, `add` significaría **sumar** los números.

### Paso 3: Actualizar los Nodos
Ahora, cada nodo puede devolver una entrada para `logs` sin miedo a borrar lo que escribieron los nodos anteriores.

```python
def extract_participants(state: State) -> State:
    # ... lógica de extracción ...
    return {
        'participants': participants,
        'logs': ["Paso 1: Extracción de participantes completada"]
    }

def identify_topics(state: State) -> State:
    # ... lógica de identificación ...
    return {
        'topics': topics,
        'logs': ["Paso 2: Temas identificados satisfactoriamente"]
    }
```

### Paso 4: Inicialización y Visualización
Al invocar el grafo, inicializamos los logs como una lista vacía. Al final de la ejecución, veremos que la lista contiene todos los mensajes acumulados.

```python
# Estado inicial
initial_state = {
    "notes": notes,
    "logs": [] # Empezamos con una lista vacía
}

# Al final, los logs se verán así:
# ["Paso 1: ...", "Paso 2: ...", "Paso 3: ..."]
```

---

## 4. Funciones Reductoras Personalizadas

Aunque en el 80-90% de los casos las funciones predefinidas como `operator.add` serán suficientes, podéis crear vuestras propias reductoras si necesitáis una lógica más específica:

```python
def mi_reductor_personalizado(current_value, new_value):
    # Lógica para combinar los valores
    return current_value + [f"LOG_NUEVO: {v}" for v in new_value]

class State(TypedDict):
    logs: Annotated[List[str], mi_reductor_personalizado]
```
---

## 5. Otras Funciones Reductoras Comunes

Aunque `operator.add` es la más utilizada para listas y contadores, existen otras formas de "reducir" o combinar el estado:

### A. Fusión de Diccionarios (Update)
Si quieres que varios nodos aporten metadatos a un mismo diccionario:

```python
def merge_dicts(existing: dict, new: dict) -> dict:
    return {**existing, **new}

class State(TypedDict):
    config: Annotated[dict, merge_dicts]
```

### B. Selección de Valores (Máximos o Mínimos)
Ideal para quedarte con la puntuación más alta de varias evaluaciones:

```python
class State(TypedDict):
    max_score: Annotated[float, max]
```

### C. Historial Limitado (Buffer)
Para evitar que una lista crezca demasiado, guardando solo los últimos N elementos:

```python
def keep_last_five(current: list, new: list) -> list:
    return (current + new)[-5:]

class State(TypedDict):
    recent_history: Annotated[list, keep_last_five]
```

---

## 6. Resumen de Combinaciones Comunes

| Tipo de Dato | Función Reductora | Comportamiento |
| :--- | :--- | :--- |
| **Listas** | `operator.add` | Acumular elementos en la lista. |
| **Números** | `operator.add` | Sumar los valores. |
| **Diccionarios** | `lambda a, b: {**a, **b}` | Combinar claves y valores. |
| **Cualquiera** | `max` / `min` | Elegir el valor más alto o más bajo. |
| **Cualquiera** | `lambda a, b: b` | **Sobrescritura** (Comportamiento por defecto). |

---

## 7. Conclusión para Estudiantes

El uso de **Annotated** no cambia el tipo de dato subyacente (sigue siendo una lista, un diccionario, etc.), sino que instruye a LangGraph sobre **cómo realizar la actualización** en el estado global. Es una herramienta fundamental para diseñar grafos donde la información fluye y se acumula de forma inteligente entre los nodos. 

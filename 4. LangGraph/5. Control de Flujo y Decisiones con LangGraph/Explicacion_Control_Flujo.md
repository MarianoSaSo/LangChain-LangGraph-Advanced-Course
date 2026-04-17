# Control de Flujo y Decisiones en LangGraph

Una de las características más poderosas de LangGraph, y lo que lo diferencia fundamentalmente de las cadenas (chains) básicas de LangChain, es su capacidad para introducir **lógica condicional** directamente en el flujo de ejecución.

En lugar de seguir una secuencia lineal fija, el grafo puede tomar decisiones basadas en el **Estado** actual y elegir diferentes caminos. Esto se logra mediante las **aristas o ejes condicionales** (`Conditional Edges`).

---

## 1. Conceptos Fundamentales

### ¿Qué es el Routing (Enrutamiento)?
El enrutamiento es el proceso de decidir qué nodo debe ejecutarse a continuación. En lugar de conectar el Nodo A con el Nodo B directamente, conectamos el Nodo A a una **función de routing**.

### La Función de Routing
Es una función de Python normal que:
1. Recibe el **Estado** actual.
2. Realiza una comprobación lógica.
3. Devuelve el **nombre del siguiente nodo** al que debe dirigirse el flujo.

---

## 2. Implementación: Ejemplo Par o Impar

Para entender la potencia del control de flujo, vamos a ver un ejemplo simplificado donde el grafo determina si un número es par o impar.

### Paso 1: Definir el Estado
Necesitamos el número de entrada y una clave para almacenar el resultado.

```python
from typing import TypedDict

class State(TypedDict):
    numero: int
    resultado: str
```

### Paso 2: Definir los Nodos de Destino
Creamos nodos que simplemente registran el resultado. Fíjate que estos nodos **no** comprueban si el número es par o no; esa lógica va en el "router".

```python
def caso_par(state: State):
    return {'resultado': 'El número es par'}

def caso_impar(state: State):
    return {'resultado': 'El número es impar'}
```

### Paso 3: Crear la Función de Routing
Aquí es donde reside la "inteligencia" del flujo.

```python
def decidir_rama(state: State):
    if state["numero"] % 2 == 0:
        return "Par"    # Nombre del nodo destino
    else:
        return "Impar"  # Nombre del nodo destino
```

---

## 3. Construcción del Grafo con `add_conditional_edges`

Para conectar el inicio del grafo con nuestra lógica de decisión, utilizamos `add_conditional_edges`.

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)

# Añadimos los nodos
graph.add_node("Par", caso_par)
graph.add_node("Impar", caso_impar)

# Añadimos la lógica condicional desde el inicio (START)
graph.add_conditional_edges(START, decidir_rama)

# Conectamos ambos casos al final de la ejecución
graph.add_edge("Par", END)
graph.add_edge("Impar", END)

compiled = graph.compile()
```

---

## 4. Ventajas frente a LangChain Tradicional

*   **Limpieza de código**: No necesitas anidar estructuras `if/else` complejas dentro de tus cadenas de Python.
*   **Eficiencia**: LangGraph gestiona la ruta de forma óptima.
*   **Escalabilidad**: Puedes añadir tantas ramas como necesites simplemente actualizando la función de routing y añadiendo los nodos correspondientes.

## Resumen
1.  **Lógica Condicional**: Permite que el grafo tome decisiones.
2.  **add_conditional_edges**: El método para añadir estas decisiones al grafo.
3.  **Router**: Función que evalúa el estado y devuelve el nombre del siguiente nodo.

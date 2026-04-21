# 🧠 Arquitectura del Estado en LangGraph (Helpdesk 2.0)

En el desarrollo de aplicaciones con **LangGraph**, el concepto más importante es el **Estado (State)**. Si el Grafo es el cuerpo de nuestra aplicación, el Estado es su **memoria compartida**.

En esta lección vamos a definir cómo se comunican nuestros nodos y qué información necesitan guardar para que un ticket de soporte pase de ser una duda a una solución.

---

## 1. La importancia de `TypedDict`

Utilizamos `TypedDict` para definir la estructura de nuestro estado. A diferencia de un diccionario normal de Python, `TypedDict` nos permite:
-   **Tipado estricto:** Definir de qué tipo es cada variable (str, int, bool).
-   **Autocompletado:** Ayuda a que el editor de código nos sugiera las claves correctas.
-   **Contrato de datos:** Asegura que todos los nodos sepan exactamente qué datos están recibiendo.

```python
class HelpdeskState(TypedDict):
    consulta: str
    # ... resto de campos
```

---

## 2. Variables del Estado (Nuestra Memoria)

Cada campo en `HelpdeskState` tiene un propósito específico en el flujo de trabajo:

| Campo | Tipo | Función |
| :--- | :--- | :--- |
| **consulta** | `str` | El problema que plantea el usuario. |
| **categoria** | `str` | Decide el camino: "automatico" o "escalado". |
| **confianza** | `float` | Determina si la IA está segura de su respuesta RAG. |
| **fuentes** | `List[str]` | Documentos usados para dar validez a la respuesta. |
| **requiere_humano** | `bool` | El interruptor que activa el Human-in-the-Loop. |
| **respuesta_final** | `Optional[str]` | Lo que finalmente recibe el usuario. |

---

## 3. El Historial Acumulativo (`Annotated` + `add`)

Esta es una de las funciones más potentes de LangGraph. Normalmente, cuando un nodo devuelve un valor, este **sobrescribe** el valor anterior en el estado. Sin embargo, para el historial queremos **acumular** información, no borrarla.

### ¿Cómo funciona el reductor `add`?
Al usar `Annotated` con la función `add`, le decimos a LangGraph: *"Cuando un nodo devuelva algo para este campo, no borres lo anterior, simplemente añádelo (concatenalo) a la lista existente"*.

```python
from operator import add
from typing import Annotated

# Este campo irá creciendo a medida que los nodos añadan sus trazas
historial: Annotated[List[str], add]
```

---

## 4. El uso de `Optional`

Verás que campos como `respuesta_rag` o `respuesta_humano` se definen como `Optional[str]`. Esto es fundamental porque:
1.  Al inicio del grafo, estas variables **no existen** (están vacías).
2.  Dependiendo de la ruta que tome el ticket (si va a un humano o no), algunas variables recibirán datos y otras se quedarán en `None`.

---

## 🚀 Resumen del Aprendizaje

- El **Estado** es la única forma que tienen los nodos de pasarse información entre sí.
- Definir un estado robusto es el **primer paso** antes de dibujar cualquier nodo o arista.
- El uso de **reductores** (`add`) permite llevar un registro de auditoría (trazas) de todo lo que sucede internamente, algo vital en entornos empresariales.

> [!TIP]
> **Consejo del Instructor:** Un buen estado debe tener solo la información necesaria. No lo llenes de variables que no vayas a usar en la lógica de decisión o en la respuesta final.

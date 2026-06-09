from langchain_core.runnables import RunnableLambda

# =========================================================
# Paso 1: Función lambda convertida en Runnable
# =========================================================
# Se define una expresión lambda muy sencilla que recibe un parámetro 'x' 
# (que asumiremos es un número) y lo convierte en una cadena de texto.
paso_uno = RunnableLambda(lambda x: f"Numero {x}")

# Es equivalente a:
#def convertir_numero(x):
   # return f"Numero {x}
#paso_uno = RunnableLambda(convertir_numero)
   #¿Qué hace RunnableLambda?
#Convierte una función normal en algo que LangChain puede usar en una cadena.


# =========================================================
# Paso 2: Función de Python tradicional convertida en Runnable
# =========================================================
# Se define una función más tradicional en Python que toma un texto como entrada,
# lo convierte en una lista y lo duplica.
def duplicar_texto(texto: str) -> list[str]:
    return [texto, texto]

# Se convierte la función a un objeto Runnable
paso_dos = RunnableLambda(duplicar_texto)


# =========================================================
# Combinación y ejecución de la cadena
# =========================================================
# Utilizamos el operador pipe (|) que nos provee el LangChain Expression Language (LCEL)
# para combinar ambos runnables secuencialmente.
cadena = paso_uno | paso_dos

# Se invoca la cadena pasándole el valor inicial (ej. 43)
resultado = cadena.invoke(44)

# Mostrar el resultado final obtenido después de ambos pasos
print(f"El resultado es: {resultado}")

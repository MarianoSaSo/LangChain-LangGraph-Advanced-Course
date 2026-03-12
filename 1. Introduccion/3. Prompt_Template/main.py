import os
from dotenv import load_dotenv

# 1. IMPORTACIONES CLAVE
# Importamos ChatOpenAI para interactuar con el cerebro (el modelo de lenguaje)
from langchain_openai import ChatOpenAI

# Importamos PromptTemplate desde 'langchain_core'. 
# NOTA: Usamos 'langchain_core' porque es la versión más moderna y eficiente (el núcleo de LangChain). 
# El PromptTemplate es como un "molde" para nuestras preguntas.
from langchain_core.prompts import PromptTemplate

# =================================================================
# LECCIÓN 3: PROMPT TEMPLATES Y CADENAS (LCEL)
# =================================================================

# OBJETIVO: Aprender a crear plantillas reutilizables y a conectarlas con la IA
# de forma elegante usando el lenguaje de expresiones de LangChain (LCEL).

# 1. CARGAR CONFIGURACIÓN
# Leemos el archivo .env donde guardamos nuestras llaves secretas (API Keys)
load_dotenv()

# 2. INICIALIZAR EL MODELO (EL CEREBRO)
# Creamos la instancia del modelo que queremos usar. 
# - model: El modelo específico (gpt-4o-mini es rápido y barato).
# - temperature: En 0 para que sea preciso y no "alucine" o invente cosas.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3. DEFINIR LA PLANTILLA (EL MOLDE)
# Un PromptTemplate es básicamente un texto con "huecos" que rellenaremos después.
# Los huecos se definen usando llaves como {estas}.

template_texto = """
Eres un traductor experto del español al inglés de nivel C2.
Tu tarea es traducir la frase que te proporcione el usuario.

FRASE A TRADUCIR: {frase_espanol}

REGLAS:
1. Responde ÚNICAMENTE con la traducción.
2. No añadas notas, saludos ni comentarios.
"""

# Creamos el objeto del Template
# - input_variables: Lista con los nombres de los huecos que hay en el texto.
# - template: El texto base que definimos arriba.
prompt = PromptTemplate(
    input_variables=["frase_espanol"],
    template=template_texto
)

# 4. CREAR LA CADENA (EL ENCHUFADO)
# Aquí ocurre la magia de LangChain llamada LCEL (LangChain Expression Language).
# Usamos el símbolo "|" (pipe) para decir: 
# "Toma lo que genere el prompt y pásalo directamente al modelo de lenguaje (llm)".
# Es como construir una tubería: Datos -> Prompt -> Modelo -> Respuesta.
cadena = prompt | llm

# 5. DATOS DE ENTRADA
# Definimos los datos que queremos meter en el molde.
datos_de_entrada = {"frase_espanol": "El rápido zorro marrón salta sobre el perro perezoso."}

# 6. EJECUCIÓN
print(f"--- PROCESANDO TRADUCCIÓN ---\n")

try:
    # Usamos .invoke() para enviar los datos a través de toda la cadena.
    # 1. El prompt recibe los datos y rellena el hueco.
    # 2. El texto resultante se envía al LLM automáticamente.
    # 3. Recibimos la respuesta final.
    respuesta = cadena.invoke(datos_de_entrada)
    
    print("--- RESULTADO FINAL ---")
    # 'respuesta.content' extrae solo el texto de la contestación de la IA
    print(f"Traducción: {respuesta.content}")
    
except Exception as e:
    # Siempre es bueno tener un bloque try/except para capturar errores de conexión o de API
    print(f"¡Ups! Algo salió mal: {e}")

# EXPLICACIÓN PARA LOS ESTUDIANTES:
# ¿Por qué usar esto y no solo un texto normal?
# 1. Reutilización: Puedes usar el mismo 'prompt' para miles de frases distintas.
# 2. Orden: Separas la lógica de las instrucciones (el template) de la lógica de ejecución.
# 3. Componibilidad: Gracias al "|", puedes añadir más piezas a la cadena fácilmente 
#    (por ejemplo, un validador o un formateador de salida).
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil y amigable que mantiene el contexto de la conversacion."),
    MessagesPlaceholder(variable_name="historial"),
    ("human", "{mensaje}"),
])

#Simulamos un historial de conversacion

historial_conversacion = [
    HumanMessage(content="Hola, ¿Cual es la capital de Polonia?"),
    AIMessage(content="La capital de Polonia es Varsovia."),
    HumanMessage(content="¿Y cuantos habitantes tiene?"),
    AIMessage(content="Varsovia tiene aproximadamente 1.8 millones de habitantes."),
]

mensajes = chat_prompt.format_messages(
    historial=historial_conversacion,
    mensaje="¿Puedes decirme algo interesante de su arquitectura?"
)

for m in mensajes:
    print(m)
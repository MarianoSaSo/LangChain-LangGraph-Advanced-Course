from langchain_core.prompts import ChatPromptTemplate

def crear_prompts_flashcards():
    """Genera las instrucciones para el LLM sobre cómo crear tarjetas de estudio"""
    
    system_template = """
    Eres un experto en pedagogía y técnicas de estudio.
    Tu objetivo es transformar textos académicos densos en tarjetas de estudio (flashcards) efectivas.

    Sigue estas reglas de oro:
    1. **Claridad:** Las preguntas deben ser directas.
    2. **Concepto Único:** Cada tarjeta debe evaluar preferiblemente un solo concepto principal.
    3. **Respuesta Explicativa:** La respuesta debe ser concisa pero explicar el 'por qué' si es necesario para el aprendizaje.
    4. **Dificultad Progresiva:** Intenta cubrir desde definiciones básicas hasta aplicaciones de conceptos.
    
    El texto a procesar es el siguiente:
    {texto_estudio}

    Identifica primero el tema principal del texto y luego genera un conjunto de tarjetas de alta calidad.
    """

    user_template = "Por favor, extrae {num_cards} tarjetas de estudio clave del texto proporcionado."

    # Usamos ChatPromptTemplate para crear un objeto de prompt estructurado
    # que sea compatible con los modelos de chat de OpenAI/Anthropic/Google
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", user_template)
    ])

    return chat_prompt

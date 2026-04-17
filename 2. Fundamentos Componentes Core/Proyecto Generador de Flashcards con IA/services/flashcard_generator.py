from langchain_openai import ChatOpenAI
from models.flashcard_model import FlashcardSet
from prompts.flashcard_prompts import crear_prompts_flashcards

def crear_generador_flashcards(model_name="gpt-4o-mini", temperature=0.3):
    """Configura el evaluador de flashcards con un modelo LLM y salida estructurada"""
    
    # Creamos el modelo base
    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature
    )

    # Forzamos al modelo a devolver siempre un objeto FlashcardSet (JSON estructurado)
    llm_estructurado = llm.with_structured_output(FlashcardSet)
    
    # Obtenemos el template del prompt
    prompt_template = crear_prompts_flashcards()

    # Usamos LangChain Expression Language (LCEL) para encadenar:
    # prompt -> llm_estructurado
    cadena_generacion = prompt_template | llm_estructurado

    return cadena_generacion

def generar_flashcards(texto_estudio: str, num_cards: int = 5) -> FlashcardSet:
    """Implementa la invocación de la cadena LangChain para generar las tarjetas"""
    try:
        # Obtenemos la cadena configurada
        generador = crear_generador_flashcards()

        # Invocamos la cadena enviando las variables
        # La salida ya será un objeto de tipo FlashcardSet de Pydantic
        resultado = generador.invoke({
            "texto_estudio": texto_estudio,
            "num_cards": num_cards
        })

        return resultado
    
    except Exception as e:
        print(f"❌ Error al generar flashcards: {e}")
        # Retornamos un objeto vacío o de error si falla la comunicación con el LLM
        return FlashcardSet(
            cards=[],
            tema_general=f"Error al procesar: {str(e)}"
        )

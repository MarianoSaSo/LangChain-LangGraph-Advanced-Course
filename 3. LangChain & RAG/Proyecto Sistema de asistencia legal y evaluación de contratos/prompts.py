# =================================================================
# PROMPTS - Plantillas de texto para el Sistema RAG
# =================================================================
# Aquí separamos TODOS los prompts del código funcional.
# Esta es una buena práctica: si quieres afinar cómo responde la IA,
# vienes a este archivo y modificas el texto sin tocar la lógica.
#

# Cada prompt tiene variables dinámicas entre {llaves} que serán
# reemplazadas automáticamente por PromptTemplate en rag_system.py.
# =================================================================


# -----------------------------------------------------------------
# PROMPT PRINCIPAL: Generación final de la respuesta RAG
# -----------------------------------------------------------------
# Este prompt recibe:
#   {context}  → Los fragmentos relevantes recuperados del vector store
#   {question} → La pregunta original del usuario
# Y le pide al LLM que responda SOLO con la información de los fragmentos
RAG_TEMPLATE = """Eres un asistente legal especializado en contratos de arrendamiento.
Basándote ÚNICAMENTE en los siguientes fragmentos de contratos, responde a la pregunta del usuario.

FRAGMENTOS DE CONTRATOS:
{context}

PREGUNTA: {question}

INSTRUCCIONES:
- Proporciona una respuesta clara y directa basada en la información disponible
- Si encuentras la información exacta, cítala textualmente cuando sea relevante
- Incluye todos los detalles importantes: nombres, direcciones, importes, fechas
- Si la información está incompleta o no está disponible, indícalo claramente
- Organiza la información de manera estructurada si es necesaria
- Si hay múltiples contratos o personas mencionadas, especifica a cuál te refieres

RESPUESTA:"""


# -----------------------------------------------------------------
# PROMPT PARA MULTI QUERY RETRIEVER: Reformulación inteligente
# -----------------------------------------------------------------
# Este prompt personaliza cómo el MultiQueryRetriever genera variaciones
# de la consulta del usuario. En lugar de usar el prompt genérico por
# defecto, le damos contexto legal para que las variaciones sean
# más inteligentes (sinónimos legales, nombres parciales, etc.)
MULTI_QUERY_PROMPT = """Eres un experto en análisis de documentos legales especializados en contratos de arrendamiento.
Tu tarea es generar múltiples versiones de la consulta del usuario para recuperar documentos relevantes desde una base de datos vectorial.

Al generar variaciones de la consulta, considera:
- Diferentes formas de referirse a personas (nombre completo, apellidos, solo nombre)
- Sinónimos legales y términos técnicos de arrendamiento
- Variaciones en la formulación de preguntas sobre aspectos contractuales
- Términos relacionados con ubicaciones, propiedades y condiciones del contrato

Consulta original: {question}

Genera exactamente 3 versiones alternativas de esta consulta, una por línea, sin numeración ni viñetas:"""


# -----------------------------------------------------------------
# PROMPT PARA ANÁLISIS DE RELEVANCIA (uso futuro / extensión)
# -----------------------------------------------------------------
# Se puede usar para filtrar fragmentos no relevantes antes de enviarlos
# al LLM final, ahorrando tokens y mejorando la precisión.
RELEVANCE_PROMPT = """Analiza si el siguiente fragmento de documento es relevante para responder la consulta del usuario.

FRAGMENTO:
{document}

CONSULTA: {question}

¿Es este fragmento relevante para responder la consulta? Responde solo con "SÍ" o "NO" y una breve justificación."""


# -----------------------------------------------------------------
# PROMPT PARA EXTRACCIÓN DE ENTIDADES (uso futuro / extensión)
# -----------------------------------------------------------------
# Se puede usar para enriquecer cada fragmento con metadatos extraídos
# por IA (personas, importes, fechas...) y mejorar las búsquedas.
ENTITY_EXTRACTION_PROMPT = """Extrae las entidades clave del siguiente texto de contrato de arrendamiento:

TEXTO:
{text}

Identifica y extrae:
- Nombres de personas (arrendador, arrendatario, avalistas)
- Direcciones de propiedades
- Importes monetarios
- Fechas importantes
- Duración del contrato
- Tipo de propiedad

Formato de respuesta:
PERSONAS: [lista de nombres]
DIRECCIONES: [lista de direcciones]
IMPORTES: [lista de cantidades]
FECHAS: [lista de fechas]
DURACIÓN: [periodo del contrato]
TIPO: [tipo de propiedad]"""
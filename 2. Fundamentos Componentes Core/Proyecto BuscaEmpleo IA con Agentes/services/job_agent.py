from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch


from langchain_core.prompts import ChatPromptTemplate
from models.job_models import JobSearchResponse
import os

def buscar_y_comparar_empleos(texto_cv: str, ubicacion_preferida: str = "remoto"):
    """
    Agente que busca ofertas de empleo reales y las compara con el CV.
    """
    
    # 1. Configurar el LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # 2. Configurar la herramienta de búsqueda Tavily
    # Usaremos k=5 para obtener hasta 5 resultados por búsqueda
    search_tool = TavilySearch(k=5)


    # 3. Paso 1: Extraer perfil y crear búsqueda
    print("🤖 Analizando perfil y creando estrategias de búsqueda...")
    prompt_search = ChatPromptTemplate.from_template("""
    Analiza este CV y genera las 3 mejores cadenas de búsqueda (en español o inglés) 
    para encontrar ofertas de trabajo actuales en LinkedIn, Infojobs o portales similares 
    que encajen perfectamente con este candidato.
    
    Ubicación preferida del usuario: {ubicacion}
    CV:
    {cv}
    
    Devuelve solo las 3 frases de búsqueda separadas por comas.
    """)
    
    chain_search = prompt_search | llm
    queries_raw = chain_search.invoke({"cv": texto_cv, "ubicacion": ubicacion_preferida}).content
    queries = [q.strip() for q in queries_raw.split(",")]

    # 4. Paso 2: Ejecutar búsquedas
    console_out = f"Buscando para: {queries}"
    print(console_out)
    
    all_results = []
    for q in queries:
        try:
            results = search_tool.invoke({"query": q})
            all_results.extend(results)
        except Exception as e:
            print(f"Error en búsqueda: {e}")

    # 5. Paso 3: Analizar resultados y hacer el Match
    print("📊 Comparando ofertas encontradas con el CV...")
    
    prompt_match = ChatPromptTemplate.from_template("""
    Eres un Headhunter de IA. Tienes el siguiente CV de un candidato y una lista de resultados de búsqueda web con ofertas de trabajo.
    
    CV del Candidato:
    {cv}
    
    Resultados de búsqueda (título y descripción corta):
    {resultados}
    
    Tu tarea es:
    1. Filtrar los resultados para quedarte con las ofertas reales de trabajo más parecidas al perfil.
    2. Comparar cada oferta con el CV y asignarle un porcentaje de compatibilidad (0-100).
    3. Explicar brevemente por qué es una buena opción (la razón).
    4. Redactar una **Carta de Presentación** para cada oferta, de no más de 2 párrafos, enfocada en cómo las habilidades del CV solucionan las necesidades de la oferta. Debe ser profesional y estar lista para copiar y enviar.
    5. Resumir brevemente el perfil profesional que has extraído del CV.

    
    Devuelve un objeto estructurado según el esquema proporcionado.
    """)
    
    llm_estructurado = llm.with_structured_output(JobSearchResponse)
    
    chain_match = prompt_match | llm_estructurado
    
    # Convertimos los resultados de búsqueda en un string legible
    contexto_busqueda = ""
    for r in all_results:
        # Si es un diccionario (formato antiguo)
        if isinstance(r, dict):
            contexto_busqueda += f"- Título/Snippet: {r.get('content', 'Sin contenido')}\n- Enlace: {r.get('url', 'Sin enlace')}\n\n"
        # Si es un objeto Document (formato estándar de LangChain)
        elif hasattr(r, 'page_content'):
            url = r.metadata.get('url', 'Sin enlace') if hasattr(r, 'metadata') else 'Sin enlace'
            contexto_busqueda += f"- Título/Snippet: {r.page_content}\n- Enlace: {url}\n\n"
        # Si es solo un string (formato simplificado)
        else:
            contexto_busqueda += f"- Información: {str(r)}\n\n"

    resultado_final = chain_match.invoke({
        "cv": texto_cv,
        "resultados": contexto_busqueda
    })


    return resultado_final

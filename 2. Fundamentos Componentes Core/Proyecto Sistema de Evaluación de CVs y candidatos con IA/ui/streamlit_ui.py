import streamlit as st
from models.cv_model import AnalisisCV
from services.pdf_processor import extraer_texto_pdf
from services.cv_evaluator import evaluar_candidato

def main():
    """Función principal que define la interfaz de usuario de Streamlit"""
    
    # st.set_page_config: Configura la pestaña del navegador web (título, icono) 
    # y cómo se usa el ancho entero de la pantalla de la web (layout="wide")
    st.set_page_config(
        page_title="Sistema de Evaluación de CVs",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # st.title: Renderiza un encabezado enorme de nivel 1 (h1) en la parte superior.
    st.title("📄 Sistema de Evaluación de CVs con IA")
    
    # st.markdown: Permite escribir texto en pantalla usando formato Markdown estándar 
    # (por ejemplo, doble asterisco para **negrita** o guiones para listas planas).
    st.markdown("""
    **Analiza currículums y evalúa candidatos de manera objetiva usando IA**
    
    Este sistema utiliza inteligencia artificial para:
    - Extraer información clave de currículums en PDF
    - Analizar la experiencia y habilidades del candidato
    - Evaluar el ajuste al puesto específico
    - Proporcionar recomendaciones objetivas de contratación
    """)
    
    # st.divider: Dibuja una línea horizontal separadora en la pantalla (como <hr> en HTML).
    st.divider()
    
    # st.columns: Divide horizontalmente la pantalla. 
    # El array [1, 1] indica que queremos 2 columnas de idéntico tamaño (50% y 50%).
    # Si pusiéramos [1, 2], la segunda sería el doble de grande que la primera.
    col_entrada, col_resultado = st.columns([1, 1], gap="large")
    
    # Utilizando 'with' indicamos a Streamlit que pinte el interior dentro de SU columna respectiva.
    with col_entrada:
        procesar_entrada()
    
    with col_resultado:
        mostrar_area_resultados()

def procesar_entrada():
    """Maneja la entrada de datos del usuario"""
    
    # st.header: Renderiza un encabezado de nivel 2 (h2). Más pequeño que st.title.
    st.header("📋 Datos de Entrada")
    
    # st.file_uploader: Crea un área de "Arrastrar y soltar" o explorar archivos de tu PC.
    # El type=['pdf'] bloquea que el usuario suba imágenes, excel o words.
    archivo_cv = st.file_uploader(
        "**1. Sube el CV del candidato (PDF)**",
        type=['pdf'],
        help="Selecciona un archivo PDF que contenga el currículum a evaluar. Asegúrate de que el texto sea legible y no esté en formato de imagen."
    )
    
    # Comprobamos lógicamente en Python que el usuario efectivamente subió algo
    if archivo_cv is not None:
        # st.success: Crea un cajón de texto verde de "éxito" para feedback positivo.
        st.success(f"✅ Archivo cargado: {archivo_cv.name}")
        # st.info: Crea un cajón de texto azul de "información genérica".
        st.info(f"📊 Tamaño: {archivo_cv.size:,} bytes")
    
    st.markdown("---")
    
    st.markdown("**2. Descripción del puesto de trabajo**")
    
    # st.text_area: Muestra un contenedor muy grande (multilínea) para introducir texto extenso,
    # en contraposición al de una sola línea llamado 'st.text_input'.
    descripcion_puesto = st.text_area(
        "Detalla los requisitos, responsabilidades y habilidades necesarias:",
        height=250,
        placeholder="""Ejemplo detallado:

**Puesto:** Desarrollador Frontend Senior

**Requisitos obligatorios:**
- 3+ años de experiencia en desarrollo frontend
- Dominio de React.js y JavaScript/TypeScript
- Experiencia con HTML5, CSS3 y frameworks CSS (Bootstrap, Tailwind)
- Conocimiento de herramientas de build (Webpack, Vite)

**Requisitos deseables:**
- Experiencia con Next.js o similares
- Conocimientos de testing (Jest, Cypress)
- Familiaridad con metodologías ágiles
- Inglés intermedio-avanzado

**Responsabilidades:**
- Desarrollo de interfaces de usuario responsivas
- Colaboración con equipos de diseño y backend
- Optimización de rendimiento de aplicaciones web
- Mantenimiento de código legacy""",
        help="Sé específico sobre requisitos técnicos, experiencia requerida y responsabilidades del puesto."
    )
    
    st.markdown("---")
    
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        # st.button: Crea un botón clicable. 
        # Devuelve 'True' únicamente en el fotograma/instante en que el usuario lo pulsa.
        # use_container_width=True hace que el botón se expanda a lo ancho ocupando toda su columna.
        # type="primary" lo colorea del color destacado del tema de Streamlit (habitualmente rosado/rojo).
        analizar = st.button(
            "🔍 Analizar Candidato", 
            type="primary",
            use_container_width=True
        )
    
    with col_btn2:
        if st.button(
            "🗑️ Limpiar", 
            use_container_width=True):
            # st.rerun: Detiene la ejecución en seco y vuelve a reiniciar la aplicación 
            # desde la línea 1 limpiando cualquier estado temporal no persistente.
            st.rerun()
    
    # st.session_state: Es el "almacenaje de variables global" de la aplicación.
    # Dado que Streamlit re-ejecuta TODO EL CÓDIGO cada vez que haces clic en un botón, 
    # usar st.session_state nos asegura que las variables persistan o viajen a lo largo del tiempo.
    st.session_state['archivo_cv'] = archivo_cv
    st.session_state['descripcion_puesto'] = descripcion_puesto
    st.session_state['analizar'] = analizar

def mostrar_area_resultados():
    """Muestra el área de resultados del análisis"""
    
    st.header("📊 Resultado del Análisis")
    
    # st.session_state.get() saca las variables globales temporales guardadas para ver si el botón fue pulsado
    if st.session_state.get('analizar', False):
        archivo_cv = st.session_state.get('archivo_cv')
        descripcion_puesto = st.session_state.get('descripcion_puesto', '').strip()
        
        if archivo_cv is None:
            # st.error: Crea un cajón rojo de "Error visual" que suele venir acompañado con su símbolo alertado.
            st.error("⚠️ Por favor sube un archivo PDF con el currículum")
            return
            
        if not descripcion_puesto:
            st.error("⚠️ Por favor proporciona una descripción detallada del puesto")
            return
        
        procesar_analisis(archivo_cv, descripcion_puesto)
    else:
        st.info("""
        👆 **Instrucciones:**
        
        1. Sube un CV en formato PDF en la columna izquierda
        2. Describe detalladamente el puesto de trabajo
        3. Haz clic en "Analizar Candidato"
        4. Aquí aparecerá el análisis completo del candidato
        
        **Consejos para mejores resultados:**
        - Usa CVs con texto seleccionable (no imágenes escaneadas)
        - Sé específico en la descripción del puesto
        - Incluye tanto requisitos obligatorios como deseables
        """)

def procesar_analisis(archivo_cv, descripcion_puesto):
    """Procesa el análisis completo del CV"""
    
    # st.spinner: Mientras lo que haya 'dentro de su with' siga cargando (en este caso consultar el LLM), 
    # Streamlit mostrará el icono dinámico de ruedita / cargando en pantalla.
    with st.spinner("🔄 Procesando currículum..."):
        
        # st.progress: Muestra una barra literal del 0% al 100% ideal para procesos por lotes.
        progress_bar = st.progress(0)
        
        # st.empty: Crea un "contenedor/hueco en blanco" en el DOM / pantalla. 
        # Útil para que después podamos ir actualizando dinámicamente el mismo hueco en vez de renderizar texto una y otra vez hacia abajo.
        status_text = st.empty()
        
        status_text.text("📄 Extrayendo texto del PDF...")
        progress_bar.progress(25)
        
        texto_cv = extraer_texto_pdf(archivo_cv)
        
        if texto_cv.startswith("Error"):
            st.error(f"❌ {texto_cv}")
            return
        
        status_text.text("🤖 Preparando análisis con IA...")
        progress_bar.progress(50)
        
        status_text.text("📊 Analizando candidato...")
        progress_bar.progress(75)
        
        resultado = evaluar_candidato(texto_cv, descripcion_puesto)
        
        status_text.text("✅ Análisis completado")
        progress_bar.progress(100)
        
        # Llamar a empty() "borra" visualmente ese contenedor de la pantalla para dejar limpieza visual una vez cargado.
        progress_bar.empty()
        status_text.empty()
        
        mostrar_resultados(resultado)

def mostrar_resultados(resultado: AnalisisCV):
    """Muestra los resultados del análisis de manera estructurada y profesional"""
    
    # st.subheader: Un encabezado de Nivel 3 (h3). Mucho más pequeño, para subniveles.
    st.subheader("🎯 Evaluación Principal")
    
    if resultado.porcentaje_ajuste >= 80:
        color = "🟢"
        nivel = "EXCELENTE"
        mensaje = "Candidato altamente recomendado"
    elif resultado.porcentaje_ajuste >= 60:
        color = "🟡"
        nivel = "BUENO"
        mensaje = "Candidato recomendado con reservas"
    elif resultado.porcentaje_ajuste >= 40:
        color = "🟠"
        nivel = "REGULAR"
        mensaje = "Candidato requiere evaluación adicional"
    else:
        color = "🔴"
        nivel = "BAJO"
        mensaje = "Candidato no recomendado"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # st.metric: Uno de los widgets más "bonitos y corporativos" de Streamlit. Sirve para mostrar KPIs (datos numéricos grandes).
        # - label: El subtítulo bajito
        # - value: el Numerazo central (En este caso del Pydantic de la IA devuelto)
        # - delta: Un indicador positivo/negativo debajo con una flecha verde o roja automáticamente.
        st.metric(
            label="Porcentaje de Ajuste al Puesto",
            value=f"{resultado.porcentaje_ajuste}%",
            delta=f"{color} {nivel}"
        )
        st.markdown(f"**{mensaje}**")
    
    st.divider()
    
    st.subheader("👤 Perfil del Candidato")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**👨‍💼 Nombre:** {resultado.nombre_candidato}")
        st.info(f"**⏱️ Experiencia:** {resultado.experiencia_años} años")
    
    with col2:
        st.info(f"**🎓 Educación:** {resultado.education}")
    
    st.subheader("💼 Experiencia Relevante")
    st.info(f"📋 **Resumen de experiencia:**\n\n{resultado.experiencia_relevante}")
    
    st.divider()
    
    st.subheader("🛠️ Habilidades Técnicas Clave")
    if resultado.habilidades_clave:
        cols = st.columns(min(len(resultado.habilidades_clave), 4))
        for i, habilidad in enumerate(resultado.habilidades_clave):
            with cols[i % 4]:
                st.success(f"✅ {habilidad}")
    else:
        # st.warning: Caja de texto amarilla de precaución/aviso por si la IA no saca variables.
        st.warning("No se identificaron habilidades técnicas específicas")
    
    st.divider()
    
    col_fortalezas, col_mejoras = st.columns(2)
    
    with col_fortalezas:
        st.subheader("💪 Fortalezas Principales")
        if resultado.fortalezas:
            for i, fortaleza in enumerate(resultado.fortalezas, 1):
                st.markdown(f"**{i}.** {fortaleza}")
        else:
            st.info("No se identificaron fortalezas específicas")
    
    with col_mejoras:
        st.subheader("📈 Áreas de Desarrollo")
        if resultado.areas_mejora:
            for i, area in enumerate(resultado.areas_mejora, 1):
                st.markdown(f"**{i}.** {area}")
        else:
            st.info("No se identificaron áreas de mejora específicas")
    
    st.divider()
    
    st.subheader("📋 Recomendación Final")
    
    if resultado.porcentaje_ajuste >= 70:
        st.success("""
        ✅ **CANDIDATO RECOMENDADO**
        
        El perfil del candidato está bien alineado con los requisitos del puesto. 
        Se recomienda proceder con las siguientes etapas del proceso de selección.
        """)
    elif resultado.porcentaje_ajuste >= 50:
        st.warning("""
        ⚠️ **CANDIDATO CON POTENCIAL**
        
        El candidato muestra potencial pero requiere evaluación adicional. 
        Se recomienda una entrevista técnica para validar competencias específicas.
        """)
    else:
        st.error("""
        ❌ **CANDIDATO NO RECOMENDADO**
        
        El perfil no se alinea suficientemente con los requisitos del puesto. 
        Se recomienda continuar la búsqueda de candidatos más adecuados.
        """)
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Guardar Análisis", use_container_width=True):
            st.info("Funcionalidad de guardado - En desarrollo")
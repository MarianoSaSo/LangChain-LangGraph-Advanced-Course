import streamlit as st
import pandas as pd
from services.pdf_processor import extraer_texto_pdf
from services.job_agent import buscar_y_comparar_empleos
from models.job_models import JobSearchResponse

def main():
    """Interfaz de usuario para el Buscador de Empleo con IA"""
    
    # 1. Configuración de página con un estilo corporativo y profesional
    st.set_page_config(
        page_title="BuscaEmpleo IA - Tu Cazatalentos de IA",
        page_icon="🔍",
        layout="wide"
    )

    # 2. Estilos personalizados para un acabado PREMIUM
    st.markdown("""
    <style>
    .job-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #007bff;
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .compatibility-high { color: #28a745; font-weight: bold; }
    .compatibility-medium { color: #fd7e14; font-weight: bold; }
    .compatibility-low { color: #dc3545; font-weight: bold; }
    .job-title { font-size: 1.25rem; font-weight: bold; color: #343a40; }
    .job-company { font-size: 1rem; color: #6c757d; }
    .job-reason { font-size: 0.9rem; font-style: italic; color: #495057; background: #e9ecef; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

    # 3. Encabezado principal
    st.title("🔍 BuscaEmpleo IA: Tu Agente Cazatalentos Personal")
    st.markdown("""
    Sube tu currículum y deja que nuestra IA busque por ti las mejores ofertas reales en portales actuales (LinkedIn, Infojobs, etc.).
    **¡No pierdas el tiempo en ofertas que no encajan contigo!**
    """)
    st.divider()

    # 4. Área de entrada de datos (Columnas)
    col_input, col_results = st.columns([1, 2], gap="large")

    with col_input:
        st.header("📋 Sube tu Perfil")
        archivo_cv = st.file_uploader("1. Sube tu CV (PDF)", type=['pdf'])
        ubicacion = st.text_input("2. Preferencia de ubicación", value="Madrid - Remoto")
        
        btn_buscar = st.button("🚀 Buscar Mejores Ofertas", type="primary", use_container_width=True)

    with col_results:
        st.header("📊 Mejores Ofertas para ti")
        
        if btn_buscar:
            if archivo_cv is not None:
                with st.spinner("🔄 El Agente está analizando tu perfil y buscando en la red..."):
                    try:
                        texto_cv = extraer_texto_pdf(archivo_cv)
                        resultado = buscar_y_comparar_empleos(texto_cv, ubicacion)
                        
                        if resultado and resultado.ofertas:
                            # Guardamos en session_state por si re-renderiza
                            st.session_state['res_empleo'] = resultado
                            st.success(f"✅ ¡Hemos encontrado {len(resultado.ofertas)} ofertas excelentes!")
                        else:
                            st.warning("⚠️ No se han encontrado ofertas que encajen hoy. ¡Inténtalo de nuevo mañana!")
                    except Exception as e:
                        st.error(f"❌ Error durante la búsqueda: {e}")
            else:
                st.info("👆 Por favor sube tu currículum para que el agente pueda trabajar.")

        # Mostrar resultados si existen
        if 'res_empleo' in st.session_state:
            mostrar_resultados(st.session_state['res_empleo'])
        else:
            st.info("Aquí aparecerán las ofertas más compatibles cuando termines el proceso.")

def mostrar_resultados(resultado: JobSearchResponse):
    """Renderiza las ofertas de trabajo encontradas"""
    
    st.markdown(f"**🔍 Perfil Profesional detectado:** {resultado.perfil_extraido}")
    st.divider()

    # Recorremos la lista de ofertas con un índice para evitar duplicados en Streamlit
    for i, oferta in enumerate(resultado.ofertas):
        # Lógica de color de compatibilidad
        comp_class = "compatibility-high" if oferta.compatibilidad >= 75 else "compatibility-medium" if oferta.compatibilidad >= 50 else "compatibility-low"
        
        # Tarjeta de Oferta con HTML
        with st.container():
            st.markdown(f"""
            <div class="job-card">
                <div class="job-title">{oferta.titulo}</div>
                <div class="job-company">🏢 {oferta.empresa} | 📍 {oferta.ubicacion}</div>
                <hr>
                <div style="margin: 10px 0;">
                    <span class="{comp_class}">🔥 Nivel de Match: {oferta.compatibilidad}%</span>
                </div>
                <div class="job-reason">
                    <strong>¿Por qué encaja contigo?</strong><br>
                    {oferta.razon}
                </div>
                <br>
                <a href="{oferta.enlace}" target="_blank" style="text-decoration: none;">
                    <button style="background-color: #007bff; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer;">
                        🌐 Ver Oferta Directa
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

            # Usamos un expander para la carta de presentación con una llave ÚNICA usando 'i'
            with st.expander(f"📄 Ver Carta de Presentación Personalizada para esta oferta"):
                st.info("Copia este texto y envíalo junto a tu CV:")
                st.text_area("Carta de Presentación:", value=oferta.carta_presentacion, height=200, key=f"carta_{i}")
                if st.button("📋 ¡Copiar al Portapapeles!", key=f"copy_{i}"):
                    st.write("Copia el texto arriba manual por ahora (Limitación de Streamlit)")



if __name__ == "__main__":
    main()

import streamlit as st
from services.pdf_processor import extraer_texto_pdf
from services.flashcard_generator import generar_flashcards
from models.flashcard_model import FlashcardSet, Flashcard

def main():
    """Interfaz de usuario para el Generador de Flashcards"""
    
    # 1. Configuración de página con un estilo premium
    st.set_page_config(
        page_title="Flashcards AI - Tu Profesor Personal",
        page_icon="🎓",
        layout="centered", # Centrado para enfocar la atención en el estudio
        initial_sidebar_state="collapsed"
    )

    # 2. Estilos CSS personalizados para que se vea INCREÍBLE
    st.markdown("""
    <style>
    /* Estilo de la tarjeta principal */
    .flashcard-box {
        background-color: #ffffff;
        border-right: 5px solid #ff4b4b;
        border-bottom: 5px solid #ff4b4b;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 30px;
        margin-bottom: 30px;
        transition: transform 0.3s;
    }
    .flashcard-box:hover {
        transform: scale(1.02);
    }
    .flash-status {
        font-family: 'Outfit', sans-serif;
        color: #ff4b4b;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }
    .flash-question {
        font-size: 1.4rem;
        color: #1e1e1e;
        margin-top: 10px;
        margin-bottom: 20px;
        font-weight: 600;
    }
    .flash-answer {
        background-color: #f7f9fc;
        border-radius: 10px;
        padding: 20px;
        font-size: 1.1rem;
        color: #334155;
        border-left: 4px solid #3b82f6;
    }
    .concept-tag {
        background-color: #e2e8f0;
        color: #475569;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 3. Título y cabecera
    st.title("🎓 Generador de Flashcards con IA")
    st.markdown("Convierte cualquier PDF de tus estudios en tarjetas de aprendizaje dinámicas para practicar y memorizar.")
    st.divider()

    # 4. Inicialización de estados de la sesión (Session State) 
    # Para que las tarjetas no se borren en cada interacción de botones/checkboxes
    if 'flashcards' not in st.session_state:
        st.session_state['flashcards'] = None
    if 'current_index' not in st.session_state:
        st.session_state['current_index'] = 0

    # 5. Area de subida de archivos
    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            archivo_subido = st.file_uploader(
                "Sube tu temario de estudio (PDF)", 
                type=['pdf'],
                help="Selecciona un PDF con tus apuntes para que la IA los procese."
            )
        with col2:
            num_cards = st.number_input("Número de tarjetas", min_value=1, max_value=15, value=5)
            generar_btn = st.button("🚀 Generar Flashcards", type="primary", use_container_width=True)

    # 6. Lógica de Activación
    if generar_btn:
        if archivo_subido is not None:
            with st.spinner("🔄 Leyendo archivo y generando tarjetas..."):
                texto = extraer_texto_pdf(archivo_subido)
                if texto.startswith("Error"):
                    st.error(texto)
                else:
                    try:
                        flashcard_data = generar_flashcards(texto, num_cards)
                        if flashcard_data.cards:
                            st.session_state['flashcards'] = flashcard_data
                            st.session_state['current_index'] = 0
                            st.rerun()
                        else:
                            st.warning("⚠️ No se pudieron generar tarjetas. Asegúrate de que el documento tenga suficiente texto.")
                    except Exception as e:
                        st.error(f"❌ Error durante la generación: {e}")
        else:
            st.warning("📥 Por favor, sube un archivo PDF primero.")

    # 7. Visualización de Resultados - El Modo Estudio
    if st.session_state['flashcards']:
        mostrar_modo_estudio(st.session_state['flashcards'])

def mostrar_modo_estudio(flashcard_set: FlashcardSet):
    """Renderiza las flashcards generadas de una manera amigable"""
    
    st.divider()
    st.subheader(f"📚 Tema: {flashcard_set.tema_general}")
    st.markdown("Haz clic en cada tarjeta para ver la respuesta")

    # Recorremos cada una de las tarjetas generadas
    for i, card in enumerate(flashcard_set.cards, 1):
        # Usamos un expander para simular la "vuelta" de la tarjeta
        with st.container():
            # Construimos la caja HTML personalizada
            st.markdown(f"""
            <div class="flashcard-box">
                <span class="flash-status">TARJETA {i}</span><br>
                <div class="concept-tag">🏷️ {card.concepto_clave}</div>
                <div class="flash-question">{card.pregunta}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botón o checkbox para revelar la respuesta sin que se sienta como un formulario
            if st.checkbox(f"Ojo... 🤔 Ver Respuesta ({i})", key=f"ans_{i}"):
                st.markdown(f"""
                <div class="flash-answer">
                    <strong>💡 Respuesta:</strong><br>
                    {card.respuesta}
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")

    # Botón para descargar el PDF o exportar para futuros usos (como mejora adicional)
    if st.button("✨ ¡Terminar Sesión de Estudio!"):
        st.balloons()
        st.success("¡Buen trabajo repasando estos conceptos!")

if __name__ == "__main__":
    main()

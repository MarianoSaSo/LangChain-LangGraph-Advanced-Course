import streamlit as st
from dotenv import load_dotenv, find_dotenv
import sys
import os

# Añadimos el directorio actual al path para que los imports funcionen correctamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.streamlit_ui import main as ui_main

# Cargamos el archivo .env de la raíz del proyecto para la API KEY
# IMPORTANTE: Busca el archivo .env hacia arriba en la carpeta raíz
load_dotenv(find_dotenv())

if __name__ == "__main__":
    ui_main()

# Para arrancar la app hay que ir al directorio del proyecto y ejecutar el comando:
# 1. Activa el venv: venv\Scripts\activate
# 2. Ejecuta la app: python -m streamlit run "2. Fundamentos Componentes Core/Proyecto BuscaEmpleo IA con Agentes/main.py"

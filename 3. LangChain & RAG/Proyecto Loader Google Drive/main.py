import os
from dotenv import load_dotenv

# 1. IMPORTACIONES
# Utilizamos el GoogleDriveLoader de la librería de la comunidad.
# Nota: La transcripción menciona que pronto se moverá a 'langchain_google_community'
from langchain_community.document_loaders import GoogleDriveLoader

# =================================================================
# MINI-PROYECTO: GOOGLE DRIVE LOADER
# =================================================================

# 1. CARGAR CONFIGURACIÓN
load_dotenv()

# --- CONFIGURACIÓN DE RUTAS ---
# Determinamos la carpeta actual del script para que las rutas sean relitivas y funcionen en cualquier PC
current_dir = os.path.dirname(os.path.abspath(__file__))

# El archivo de credenciales descargado de Google Cloud Console
# ¡RECUERDA poner tu archivo JSON en esta misma carpeta!
credentials_path = os.path.join(current_dir, "credentials.json")

# El token se generará automáticamente en la primera ejecución
token_path = os.path.join(current_dir, "token.json")

# --- PARÁMETROS DE DRIVE ---
# Sustituye este ID por el de tu propia carpeta de Google Drive (el código al final de la URL)
FOLDER_ID = "145D8my3BlrplfL3m3GUN6q38dkrz0eR9" # ID de ejemplo de la lección

print("--- INICIANDO PROCESO DE AUTENTICACIÓN Y CARGA DE DRIVE ---\n")

try:
    # 2. DEFINO EL LOADER
    # Solo necesitamos las credenciales, el token y el ID de la carpeta
    loader = GoogleDriveLoader(
        folder_id=FOLDER_ID,
        credentials_path=credentials_path,
        token_path=token_path,
        recursive=False # Cambia a True si quieres leer carpetas dentro de carpetas
    )

    # 3. CARGAMOS LOS DOCUMENTOS
    # La primera vez se abrirá el navegador para pedir permiso.
    # Después usará el token.json generado.
    documents = loader.load()

    # 4. MOSTRAMOS EL RESULTADO
    if documents:
        print(f"✅ Se han cargado {len(documents)} documentos correctamente.\n")
        
        # Mostramos información del primer documento como prueba
        primer_doc = documents[0]
        print(f"--- PRIMER DOCUMENTO ---")
        print(f"Metadatos: {primer_doc.metadata}")
        print(f"Fragmento del Contenido: {primer_doc.page_content[:300]}...")
    else:
        print("⚠️ No se encontraron documentos en la carpeta indicada.")

except Exception as e:
    print(f"❌ Error al conectar con Google Drive: {e}")
    print("\nRECUERDA:")
    print("1. Debes tener el archivo 'credentials.json' en esta carpeta.")
    print("2. Debes haber habilitado la 'Google Drive API' en Google Cloud Console.")
    print("3. Debes haber añadido tu correo a 'Test Users' en la pantalla de OAuth.")
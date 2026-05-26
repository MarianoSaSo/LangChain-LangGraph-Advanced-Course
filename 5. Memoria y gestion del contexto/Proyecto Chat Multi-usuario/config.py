import os

# Configuracion de directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Obtiene el directorio base o raiz del archivo actual
DATA_DIR = os.path.join(BASE_DIR, "data") # Aqui es donde se guardaran los datos, sera como la base de datos de la aplicacion
USERS_DIR = os.path.join(BASE_DIR, "users") # Aqui es donde se guardaran los usuarios, sera como la base de datos de los usuarios

# Crar directorios si no existen
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(USERS_DIR, exist_ok=True)

# Configuracion del modelo
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.3

# Configuracion de memoria
MAX_VECTOR_RESULTS = 3
MEMORY_CATEGORIES = [ # Categorias de la memoria, sera como las categorias de la base de datos de la aplicacion
    "personal", 
    "profesional", 
    "preferencias", 
    "hechos_importantes" 
]

# Configuracion de la interfaz # Titulo de la aplicacion y icono
PAGE_TITLE = "Chat Multi-Usuario con memoria Avanzada" # Titulo de la aplicacion
PAGE_ICON = "🤖" # Icono de la aplicacion
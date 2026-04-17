from pydantic import BaseModel

# Definición de un modelo personalizado utilizando Pydantic
class Usuario(BaseModel):
    identificador: int
    nombre: str
    activo: bool = True

# Datos de prueba simulando el origen de un sistema con errores de tipado o incompletos
datos_recibidos = {
    "identificador": "123",  # Nos llega en tipo string en vez de entero
    "nombre": "Ana",
    "activo": False #T Si no pusieramos nada se pondria automaticamente un True por el valor por defecto del constructor
    # Falta el atributo "activo"
}

# Pydantic valida, convierte y transforma estos datos según el modelo definido
usuario = Usuario(**datos_recibidos)

# Imprimimos el objeto en Python (se ve cómo corrigió el integer y añadió el bool)
print("Objeto Pydantic instanciado:")
print(usuario)

# Podemos exportarlo a JSON de manera sencilla y robusta
print("\nExportación a formato JSON:")
print(usuario.model_dump_json())
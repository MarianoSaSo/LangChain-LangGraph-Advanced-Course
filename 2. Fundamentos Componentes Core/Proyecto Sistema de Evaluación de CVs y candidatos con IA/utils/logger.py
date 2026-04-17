import logging
import sys

def setup_logger(name="cv_evaluator"):
    """
    Configura un logger profesional para el proyecto.
    Esta es una gran práctica para que los estudiantes puedan ver por consola lo que está
    pasando "bajo el capó" (prompts, tiempos, errores) sin ensuciar la interfaz UI.
    """
    logger = logging.getLogger(name)
    
    # Evitamos que se dupliquen los logs si ya existe un handler activo
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Formato profesional: [HORA] | [NIVEL] | Mensaje
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%H:%M:%S'
        )

        # Handler para que los logs salgan por la consola/terminal
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Exportamos una única instancia del logger para todo el proyecto
logger = setup_logger()

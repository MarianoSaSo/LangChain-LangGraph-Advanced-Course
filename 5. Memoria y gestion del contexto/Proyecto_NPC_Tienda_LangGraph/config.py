"""
Configuración central del mini proyecto.

En proyectos reales aquí suele concentrarse: modelo por defecto, rutas,
feature flags y lectura de variables de entorno.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Raíz de este mini proyecto (carpeta que contiene main.py y este archivo)
PROJECT_ROOT = Path(__file__).resolve().parent


def _find_course_root(start: Path, max_levels: int = 12) -> Path | None:
    """
    Localiza la raíz del repositorio del curso buscando `requirements.txt`.
    Así no dependemos de contar carpetas (parents[2]), que falla si cambia la jerarquía.
    """
    cur = start.resolve()
    for _ in range(max_levels):
        if (cur / "requirements.txt").is_file():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def _load_dotenv_ascending(start: Path, max_levels: int = 8) -> None:
    """Busca .env subiendo desde `start` (sin sobrescribir variables ya definidas)."""
    cur = start.resolve()
    for _ in range(max_levels):
        candidate = cur / ".env"
        if candidate.is_file():
            load_dotenv(candidate)
            return
        if cur.parent == cur:
            break
        cur = cur.parent
    load_dotenv()


# 1) Raíz del curso = carpeta donde está requirements.txt (tu .env está ahí)
CURSO_ROOT = _find_course_root(PROJECT_ROOT) or PROJECT_ROOT.parents[2]
_root_env = CURSO_ROOT / ".env"
if _root_env.is_file():
    # override=True: el .env del curso manda aunque el sistema tenga variables vacías heredadas
    load_dotenv(_root_env, override=True)

# 2) .env local del mini proyecto (opcional; no pisa claves ya cargadas salvo que uses override)
load_dotenv(PROJECT_ROOT / ".env")

# 3) Si aún no hubo archivo en la raíz detectada, seguir buscando .env hacia arriba
if not os.getenv("OPENAI_API_KEY"):
    _load_dotenv_ascending(PROJECT_ROOT)


def get_openai_model() -> str:
    return os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")


def get_llm_temperature() -> float:
    return float(os.getenv("OPENAI_TEMPERATURE", "0.3"))

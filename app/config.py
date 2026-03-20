import logging
import sys
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Literal


# ── Structured Logging ────────────────────────────────────────────────────────

def setup_logging() -> logging.Logger:
    """Configure structured logging for the Visualization Agent."""
    logger = logging.getLogger("viz-agent")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


# ── Settings ──────────────────────────────────────────────────────────────────

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    STORAGE_TYPE: Literal["local"] = "local"
    CHART_OUTPUT_PATH: str = "./charts"
    MAX_DATA_ROWS: int = 1000
    PORT: int = 8003


settings = Settings()
logger = setup_logging()
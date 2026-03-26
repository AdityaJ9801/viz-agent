import logging
import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
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
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    LLM_PROVIDER: Literal["ollama", "openai", "anthropic", "groq", "grok"] = "ollama"
    GROQ_API_KEY: str = "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"
    XAI_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    OLLAMA_MODEL: str = ""
    OLLAMA_BASE_URL: str = ""
    STORAGE_TYPE: Literal["local"] = "local"
    CHART_OUTPUT_PATH: str = "./charts"
    MAX_DATA_ROWS: int = 1000
    PORT: int = 8003


settings = Settings()
logger = setup_logging()
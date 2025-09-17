"""Application settings and configuration helpers."""
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime application configuration."""

    database_url: str = "sqlite+aiosqlite:///./leo.db"
    database_echo: bool = False
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4.1-mini"
    openai_temperature: float = 0.3
    fallback_translation_provider: str | None = "google_translate"
    google_translate_api_key: Optional[str] = None
    default_tone: str = "professional"
    reviewer_sla_hours: int = 24
    seed_initial_glossary: bool = True
    initial_glossary_path: str = "app/data/initial_glossary.json"
    blocked_terms: list[str] = Field(default_factory=list)
    # Comma-separated or JSON list via env: LEO_CORS_ALLOWED_ORIGINS
    cors_allowed_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )

    model_config = SettingsConfigDict(
        env_prefix="LEO_",
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance."""

    return Settings()

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App configuration, read from environment variables or a .env file.

    Each field maps to an env var with the same name (case-insensitive),
    e.g. APP_NAME=... sets app_name. Pydantic converts and validates types.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Notes API"
    environment: str = "development"


@lru_cache
def get_settings() -> Settings:
    # Cached so the .env file is read once, not on every request.
    return Settings()

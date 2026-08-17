from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolved relative to this file (not the process's working directory) so
# settings load correctly regardless of where the app is launched from —
# e.g. `npm run dev` invokes uvicorn with cwd=frontend/, where a plain
# ".env" would never be found and everything would silently fall back to
# the hardcoded defaults below.
_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_ENV_FILE, env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str = "postgresql+psycopg://recall:recall@localhost:5432/recall"

    # Auth
    jwt_secret: str = "change-me-to-a-long-random-string"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # LLM providers
    openrouter_api_key: str = ""
    openrouter_model: str = "meta-llama/llama-3.1-8b-instruct"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-5"

    embedding_provider: str = "openrouter"
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536

    # App
    env: str = "development"
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

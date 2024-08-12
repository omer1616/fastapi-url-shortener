from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    APP_NAME: str = "Awesome API"
    BASE_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(env_file=".env")

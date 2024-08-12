from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Awesome API"
    BASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")
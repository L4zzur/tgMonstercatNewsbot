from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    ADMIN_IDS: int | list[int]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()

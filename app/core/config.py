from datetime import timedelta
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str = Field(validation_alias="SQL_ALCHEMY_DB_URL")
    LOG_LEVEL: str = "INFO"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRY: timedelta = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRY: timedelta = timedelta(days=1)

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()

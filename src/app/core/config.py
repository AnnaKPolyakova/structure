import os
from logging import config as logging_config
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from src.app.core.logger import LOGGING

load_dotenv()


logging_config.dictConfig(LOGGING)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):  # type: ignore[misc]
    PROJECT_NAME: str = "name"
    APP_ENV: str = "dev"
    APP_LOG_LEVEL: str = "INFO"
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6376
    REDIS_PROTOCOL: str = "redis"

    POSTGRES_PASSWORD: str = "password"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "database"
    POSTGRES_USER: str = "user"

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


settings = Settings()

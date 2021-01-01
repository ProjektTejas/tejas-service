import secrets
import sys

from pydantic import BaseSettings

from typing import Dict, Any


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(nbytes=32)

    PROJECT_NAME: str = "TejasAI"

    ALLOW_ALL_CORS: bool = True

    LOGURU_FORMAT: str = "{time} {name}.{function}.{line} [{level}]: {message}"


settings = Settings()

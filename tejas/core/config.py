import secrets
import sys
import os

from pydantic import BaseSettings
from pathlib import Path

from typing import Dict, Any


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(nbytes=32)

    PROJECT_NAME: str = "TejasAI"

    ALLOW_ALL_CORS: bool = True

    LOGURU_FORMAT: str = "{time} {name}.{function}.{line} [{level}]: {message}"

    TEJAS_MODEL_TRAIN_LAMBDA_ARN: str = os.environ["TEJAS_MODEL_TRAIN_LAMBDA_ARN"]

    TASKS_TABLE = os.environ["TASKS_TABLE"]

    #    DATASETS_PATH = Path(os.environ["TEJAS_DATASETS_PATH"])
    MODELS_PATH = Path(os.environ["TEJAS_MODELS_PATH"])

    MODELS_BUCKET: str = os.environ["TEJAS_MODELS_BUCKET"]
    DATASETS_BUCKET: str = os.environ["TEJAS_DATASETS_BUCKET"]


settings = Settings()

import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from ict_4485_week_10.models import db_models

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    mongo_api_version: int | None = 1
    mongo_db_name: str | None = "ict-4485"
    mongo_default_db_name: str | None = db_models.DbNameEnum.DEFAULT
    mongo_username: str
    mongo_password: str
    api_host: str | None = "localhost"
    api_port: int | None = 8888
    api_v1_base: str | None = "/v1/ict-4485"

    model_config = SettingsConfigDict(
        env_file=DOTENV,
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
from pydantic import MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_api_key: str
    model_name: str
    db_url: MongoDsn
    database_name: str
    ai_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra='ignore'
    )


settings = Settings()

# config.py
from pydantic import BaseSettings
class Settings(BaseSettings):
    app_name: str = "ChatBot Music AI API"
    API_KEY: str
    SEARCH_ENGINE_ID: str

    class Config:
        env_file = ".env"

settings = Settings()
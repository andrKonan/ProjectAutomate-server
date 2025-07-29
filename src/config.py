# server/src/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./game.db"

@lru_cache
def get_settings() -> Settings:
    return Settings()
# server/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./server/game.db"

settings = Settings()
# server/database.py
import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .config import settings

engine = create_async_engine(settings.db_url, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

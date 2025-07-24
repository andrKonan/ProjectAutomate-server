# server/tests/conftest.py
from typing import AsyncGenerator
import os

import pytest_asyncio
from httpx import AsyncClient
from httpx import ASGITransport

from server.main import app, lifespan
from server.database import get_db

@pytest_asyncio.fixture(scope="module")
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    async with lifespan(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client

@pytest_asyncio.fixture(scope="module", autouse=True)
async def use_test_database():
    os.environ["DB_URL"] = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async for session in get_db():
        yield session
        break  
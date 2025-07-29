from typing import AsyncGenerator
import os

import pytest_asyncio
from httpx import AsyncClient
from httpx import ASGITransport

from src.main import app, lifespan
from src.database import get_db
from tests.utils import generate_unique_name

@pytest_asyncio.fixture(scope="module")
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    async with lifespan(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client

@pytest_asyncio.fixture(scope="module")
async def auth_headers(test_client):
    variables = {"name": generate_unique_name("TestClient")}
    response = await test_client.post(
        "/graphql",
        json={"query": 
            r"""mutation Register($name: String!) {
                client {
                    create(input: {name: $name}) {
                        id
                        Token
                        name
                    }
                }
            }""", 
            "variables": variables
        },
    )
    token = response.json()["data"]["client"]["create"]["Token"]
    return {"Authorization": f"Bearer {token}"}

@pytest_asyncio.fixture(scope="module", autouse=True)
async def use_test_database():
    os.environ["DB_URL"] = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async for session in get_db():
        yield session
        break  
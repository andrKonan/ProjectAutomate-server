# server/main.py
from pathlib import Path

from contextlib import asynccontextmanager
from fastapi import FastAPI

from server.database import engine
from server.database.models import Base

from server.graphql import graphql_app
from server.workers.seed import seed_item_types

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Game server is starting up")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    seed_file = Path("server/seed/items.yaml")
    await seed_item_types(seed_file)

    yield

    print("Game server is shutting down")

app = FastAPI(lifespan=lifespan)

app.include_router(graphql_app, prefix="/graphql")
# server/main.py
from pathlib import Path

from contextlib import asynccontextmanager
from fastapi import FastAPI

from server.database import engine
from server.database.models import Base

from server.graphql import graphql_app
from server.workers.seed import run_all_seeds

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Game server is starting up")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    seed_file = Path(__file__).parent / "seed"

    await run_all_seeds(seed_file)

    print("✅ GraphiQL available at http://127.0.0.1:8000/graphql")

    yield

    print("Game server is shutting down")

app = FastAPI(lifespan=lifespan)

app.include_router(graphql_app, prefix="/graphql")
# server/src/main.py
from pathlib import Path

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database import get_engine
from src.database.models import Base

from src.graphql import graphql_app
from src.workers.seed import run_all_seeds

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Game server is starting up")
    
    local_engine = get_engine()
    async with local_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    seed_file = Path(__file__).parent / "seed"

    await run_all_seeds(seed_file)

    print("✅ GraphiQL available at http://127.0.0.1:8000/graphql")

    yield

    print("Game server is shutting down")

app = FastAPI(lifespan=lifespan)

app.include_router(graphql_app, prefix="/graphql")
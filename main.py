# server/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from server.database import engine
from server.models import Base

from server.graphql import graphql_app

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Game server is starting up")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    print("Game server is shutting down")

app = FastAPI(lifespan=lifespan)

app.include_router(graphql_app, prefix="/graphql")
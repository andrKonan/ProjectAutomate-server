# server/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from .database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Game server is starting up")
    
    yield

    print("Game server is shutting down")

app = FastAPI(lifespan=lifespan)

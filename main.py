# server/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
import strawberry
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.ext.asyncio import AsyncSession

from .database import engine, get_db
from .models import Base
from .resolvers import schema

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Game server is starting up")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    print("Game server is shutting down")

app = FastAPI(lifespan=lifespan)

async def get_context(db: AsyncSession = Depends(get_db)) -> dict:
    """
    Strawberry context getter: injects an AsyncSession as `context['db']`.
    """
    return {"db": db}

graphql_app = GraphQLRouter(schema, context_getter=get_context, graphiql=True)
app.include_router(graphql_app, prefix="/graphql")
# server/graphql.py
from fastapi import Request, Depends
import strawberry
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.ext.asyncio import AsyncSession

from server.database import get_db
from server.graphql.resolvers import Query, Mutation
from server.database.services import ClientService 

async def get_context(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Strawberry context getter: injects:
      - `db`: an AsyncSession
      - `current_client`: the Client matched by the Bearer token (or None)
    """
    # 1) grab the raw header
    auth: str = request.headers.get("Authorization", "")
    # 2) strip off "Bearer " if present
    token = auth[7:] if auth.lower().startswith("bearer ") else None

    # 3) look up the client by token (or None)
    current_client = None
    if token:
        current_client = await ClientService.get_by_token(db, token)

    return {
        "db": db,
        "current_client": current_client,
    }

graphql_app = GraphQLRouter(
    strawberry.Schema(
        query=Query, 
        mutation=Mutation
    ), 
    context_getter=get_context,
    graphiql=True
)
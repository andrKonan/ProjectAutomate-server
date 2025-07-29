# server/src/graphql/resolvers/clients.py
from uuid import UUID

import strawberry
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.services import ClientService
from src.graphql.schemas import ClientScheme
from src.graphql.inputs import ClientCreateInput, ClientUpdateInput
from src.graphql.permissions import IsAuthenticated, IsClientOwner


async def get_client_by_id(info: Info, id: UUID) -> ClientScheme:
    db: AsyncSession = info.context["db"]
    return await ClientService.get_by_id(db, id)

async def get_my_client(info: Info) -> ClientScheme:
    print(info.context)
    return info.context.get("current_client")

@strawberry.type
class ClientQuery:
    by_id: ClientScheme = strawberry.field(
        resolver=get_client_by_id,
        description="Fetch a single client by its ID",
        permission_classes=[IsAuthenticated, IsClientOwner]
    )

    me: ClientScheme = strawberry.field(
        resolver=get_my_client,
        description="Gets current client",
        permission_classes=[IsAuthenticated]
    )

async def create_client(info: Info, input: ClientCreateInput) -> ClientScheme:
    db: AsyncSession = info.context["db"]
    return await ClientService.create(db, input)

async def update_client(info: Info, input: ClientUpdateInput) -> ClientScheme:
    db: AsyncSession = info.context["db"]
    return await ClientService.update(db, input)

async def delete_client(info: Info, id: UUID) -> bool:
    db: AsyncSession = info.context["db"]
    return await ClientService.delete(db, id)

@strawberry.type
class ClientMutation:
    create: ClientScheme = strawberry.mutation(
        resolver=create_client,
        description="Create a new client"
    )

    update: ClientScheme = strawberry.mutation(
        resolver=update_client,
        description="Update an existing client",
        permission_classes=[IsAuthenticated, IsClientOwner]
    )

    delete: bool = strawberry.mutation(
        resolver=delete_client,
        description="Delete a client by its ID",
        permission_classes=[IsAuthenticated, IsClientOwner]
    )
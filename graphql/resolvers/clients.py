# server/resolvers/clients.py
import strawberry
from sqlalchemy.ext.asyncio import AsyncSession

from server.database.services import ClientService
from server.graphql.schemas.clients import ClientScheme, ClientInput
from server.graphql.permissions import IsAuthenticated, IsClientOwner


async def get_client_by_id(info, id: strawberry.ID) -> ClientScheme:
    db: AsyncSession = info.context["db"]
    return await ClientService.get_by_id(db, id)

async def get_my_client(info) -> ClientScheme:
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

async def create_client(info, input: ClientInput) -> ClientScheme:
    db: AsyncSession = info.context["db"]
    return await ClientService.create(db, input)

async def update_client(info, id: strawberry.ID, input: ClientInput) -> ClientScheme:
    db: AsyncSession = info.context["db"]
    return await ClientService.update(db, id, input)

async def delete_client(info, id: strawberry.ID) -> bool:
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
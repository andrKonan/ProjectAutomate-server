# server/resolvers/clients.py
import strawberry
from sqlalchemy.ext.asyncio import AsyncSession

from server.graphql.services import ClientService
from server.graphql.schemas.clients import ClientType, ClientInput
from server.graphql.permissions import IsAuthenticated, IsClientOwner

@strawberry.type
class ClientQuery:
    @strawberry.field(
        description="Fetch a single client by its ID",
        permission_classes=[IsAuthenticated, IsClientOwner]
    )
    async def client(self, info, id: strawberry.ID) -> ClientType:
        db: AsyncSession = info.context["db"]
        return await ClientService.get_by_id(db, id)

@strawberry.type
class ClientMutation:
    @strawberry.mutation(description="Create a new client",)
    async def create_client(
        self, info, input: ClientInput
    ) -> ClientType:
        db: AsyncSession = info.context["db"]
        return await ClientService.create(db, input)

    @strawberry.mutation(
        description="Update an existing client",
        permission_classes=[IsAuthenticated, IsClientOwner]
    )
    async def update_client(
        self, info, id: strawberry.ID, input: ClientInput
    ) -> ClientType:
        db: AsyncSession = info.context["db"]
        return await ClientService.update(db, id, input)

    @strawberry.mutation(
        description="Delete a client by its ID",
        permission_classes=[IsAuthenticated, IsClientOwner]
    )
    async def delete_client(self, info, id: strawberry.ID) -> bool:
        db: AsyncSession = info.context["db"]
        return await ClientService.delete(db, id)
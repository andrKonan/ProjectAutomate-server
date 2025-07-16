# server/resolvers/clients.py
from typing import Sequence

import strawberry
from sqlalchemy.ext.asyncio import AsyncSession

from ..services import ClientService
from ..schemas.clients import ClientType, ClientInput

@strawberry.type
class ClientQuery:
    @strawberry.field(description="Fetch a single client by its ID")
    async def client(self, info, id: strawberry.ID) -> ClientType:
        db: AsyncSession = info.context["db"]
        return await ClientService.get_by_id(db, int(id))

    @strawberry.field(description="Fetch all clients")
    async def clients(self, info) -> Sequence[ClientType]:
        db: AsyncSession = info.context["db"]
        return await ClientService.list_all(db)

@strawberry.type
class ClientMutation:
    @strawberry.mutation(description="Create a new client")
    async def create_client(
        self, info, input: ClientInput
    ) -> ClientType:
        db: AsyncSession = info.context["db"]
        return await ClientService.create(db, input)

    @strawberry.mutation(description="Update an existing client")
    async def update_client(
        self, info, id: strawberry.ID, input: ClientInput
    ) -> ClientType:
        db: AsyncSession = info.context["db"]
        return await ClientService.update(db, int(id), input)

    @strawberry.mutation(description="Delete a client by its ID")
    async def delete_client(self, info, id: strawberry.ID) -> bool:
        db: AsyncSession = info.context["db"]
        return await ClientService.delete(db, int(id))
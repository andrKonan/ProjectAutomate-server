# server/resolvers/items.py
from typing import Sequence

import strawberry
from sqlalchemy.ext.asyncio import AsyncSession

from server.database.services import ItemTypeService
from server.graphql.schemas.items import ItemTypeScheme, ItemTypeInput
from server.graphql.permissions import IsAuthenticated

@strawberry.type
class ItemTypeQuery:
    @strawberry.field(
        description="Fetch a single item type by its ID",
        permission_classes=[IsAuthenticated]
    )
    async def itemtype(self, info, id: strawberry.ID) -> ItemTypeScheme:
        db: AsyncSession = info.context["db"]
        return await ItemTypeService.get_by_id(db, id)
    
    @strawberry.field(
        description="Fetch all item types",
        permission_classes=[IsAuthenticated]
    )
    async def itemtypes(self, info) -> Sequence[ItemTypeScheme]:
        db: AsyncSession = info.context["db"]
        return await ItemTypeService.list_all(db)


@strawberry.type
class ItemTypeMutation:
    @strawberry.mutation(description="Create a new item type",)
    async def create_itemtype(
        self, info, input: ItemTypeInput
    ) -> ItemTypeScheme:
        db: AsyncSession = info.context["db"]
        return await ItemTypeService.create(db, input)

    @strawberry.mutation(
        description="Update an existing item type",
        permission_classes=[IsAuthenticated]
    )
    async def update_itemtype(
        self, info, id: strawberry.ID, input: ItemTypeInput
    ) -> ItemTypeScheme:
        db: AsyncSession = info.context["db"]
        return await ItemTypeService.update(db, id, input)

    @strawberry.mutation(
        description="Delete an item type by its ID",
        permission_classes=[IsAuthenticated]
    )
    async def delete_itemtype(self, info, id: strawberry.ID) -> bool:
        db: AsyncSession = info.context["db"]
        return await ItemTypeService.delete(db, id)
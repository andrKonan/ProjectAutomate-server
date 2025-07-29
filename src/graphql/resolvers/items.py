# server/src/graphql/resolvers/items.py
from typing import Sequence
from uuid import UUID

import strawberry
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.services import ItemTypeService
from src.graphql.schemas import ItemTypeScheme
from src.graphql.inputs import ItemTypeInput
from src.graphql.permissions import IsAuthenticated


async def get_item_type_by_id(info: Info, id: UUID) -> ItemTypeScheme:
    db: AsyncSession = info.context["db"]
    return await ItemTypeService.get_by_id(db, id)


async def list_item_types(info: Info) -> Sequence[ItemTypeScheme]:
    db: AsyncSession = info.context["db"]
    return await ItemTypeService.list_all(db)

@strawberry.type
class ItemTypeQuery:
    by_id: ItemTypeScheme = strawberry.field(
        resolver=get_item_type_by_id,
        description="Fetch a single item type by its ID",
        permission_classes=[IsAuthenticated],
    )

    all: Sequence[ItemTypeScheme] = strawberry.field(
        resolver=list_item_types,
        description="List all item types",
        permission_classes=[IsAuthenticated],
    )


async def create_item_type(info: Info, input: ItemTypeInput) -> ItemTypeScheme:
    db: AsyncSession = info.context["db"]
    return await ItemTypeService.create(db, input)

async def update_item_type(info: Info, id: UUID, input: ItemTypeInput) -> ItemTypeScheme:
    db: AsyncSession = info.context["db"]
    return await ItemTypeService.update(db, id, input)

async def delete_item_type(info: Info, id: UUID) -> bool:
    db: AsyncSession = info.context["db"]
    return await ItemTypeService.delete(db, id)


@strawberry.type
class ItemTypeMutation:
    create: ItemTypeScheme = strawberry.mutation(
        resolver=create_item_type,
        description="Create a new item type",
    )

    update: ItemTypeScheme = strawberry.mutation(
        resolver=update_item_type,
        description="Update an existing item type",
        permission_classes=[IsAuthenticated],
    )

    delete: bool = strawberry.mutation(
        resolver=delete_item_type,
        description="Delete an item type by its ID",
        permission_classes=[IsAuthenticated],
    )
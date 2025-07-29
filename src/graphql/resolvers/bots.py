# server/src/graphql/resolvers/bots.py
from typing import Sequence
from uuid import UUID

import strawberry
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.services import BotTypeService
from src.graphql.schemas import BotTypeScheme
from src.graphql.inputs import BotTypeInput
from src.graphql.permissions import IsAuthenticated


async def get_bot_type_by_id(info: Info, id: UUID) -> BotTypeScheme:
    db: AsyncSession = info.context["db"]
    return await BotTypeService.get_by_id(db, id)

async def list_bot_types(info: Info) -> Sequence[BotTypeScheme]:
    db: AsyncSession = info.context["db"]
    return await BotTypeService.list_all(db)

@strawberry.type
class BotTypeQuery:
    by_id: BotTypeScheme = strawberry.field(
        resolver=get_bot_type_by_id,
        description="Fetch a single bot type by its ID",
        permission_classes=[IsAuthenticated],
    )

    all: Sequence[BotTypeScheme] = strawberry.field(
        resolver=list_bot_types,
        description="List all bot types",
        permission_classes=[IsAuthenticated],
    )


async def create_bot_type(info: Info, input: BotTypeInput) -> BotTypeScheme:
    db: AsyncSession = info.context["db"]
    return await BotTypeService.create(db, input)

async def update_bot_type(
    info: Info, id: UUID, input: BotTypeInput
) -> BotTypeScheme:
    db: AsyncSession = info.context["db"]
    return await BotTypeService.update(db, id, input)

async def delete_bot_type(info: Info, id: UUID) -> bool:
    db: AsyncSession = info.context["db"]
    return await BotTypeService.delete(db, id)

@strawberry.type
class BotTypeMutation:
    create: BotTypeScheme = strawberry.mutation(
        resolver=create_bot_type,
        description="Create a new bot type",
    )

    update: BotTypeScheme = strawberry.mutation(
        resolver=update_bot_type,
        description="Update an existing bot type",
        permission_classes=[IsAuthenticated],
    )

    delete: bool = strawberry.mutation(
        resolver=delete_bot_type,
        description="Delete a bot type by its ID",
        permission_classes=[IsAuthenticated],
    )
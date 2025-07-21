# server/graphql/resolvers/bots.py
from typing import Sequence

import strawberry
from sqlalchemy.ext.asyncio import AsyncSession

from server.database.services import BotTypeService
from server.graphql.schemas import BotTypeScheme, BotTypeInput
from server.graphql.permissions import IsAuthenticated


async def get_bot_type_by_id(info, id: strawberry.ID) -> BotTypeScheme:
    db: AsyncSession = info.context["db"]
    return await BotTypeService.get_by_id(db, id)

async def list_bot_types(info) -> Sequence[BotTypeScheme]:
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


async def create_bot_type(info, input: BotTypeInput) -> BotTypeScheme:
    db: AsyncSession = info.context["db"]
    return await BotTypeService.create(db, input)

async def update_bot_type(
    info, id: strawberry.ID, input: BotTypeInput
) -> BotTypeScheme:
    db: AsyncSession = info.context["db"]
    return await BotTypeService.update(db, id, input)

async def delete_bot_type(info, id: strawberry.ID) -> bool:
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
# server/src/graphql/resolvers/buildings.py
from typing import Sequence
from uuid import UUID

import strawberry
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.services import BuildingTypeService
from src.graphql.schemas import BuildingTypeScheme
from src.graphql.inputs import BuildingTypeInput
from src.graphql.permissions import IsAuthenticated


async def get_building_type_by_id(info: Info, id: UUID) -> BuildingTypeScheme:
    db: AsyncSession = info.context["db"]
    return await BuildingTypeService.get_by_id(db, id)

async def list_building_types(info: Info) -> Sequence[BuildingTypeScheme]:
    db: AsyncSession = info.context["db"]
    return await BuildingTypeService.list_all(db)

@strawberry.type
class BuildingTypeQuery:
    by_id: BuildingTypeScheme = strawberry.field(
        resolver=get_building_type_by_id,
        description="Fetch a single building type by its ID",
        permission_classes=[IsAuthenticated],
    )

    all: Sequence[BuildingTypeScheme] = strawberry.field(
        resolver=list_building_types,
        description="List all building types",
        permission_classes=[IsAuthenticated],
    )


async def create_building_type(info: Info, input: BuildingTypeInput) -> BuildingTypeScheme:
    db: AsyncSession = info.context["db"]
    return await BuildingTypeService.create(db, input)

async def update_building_type(info: Info, id: UUID, input: BuildingTypeInput) -> BuildingTypeScheme:
    db: AsyncSession = info.context["db"]
    return await BuildingTypeService.update(db, id, input)

async def delete_building_type(info: Info, id: UUID) -> bool:
    db: AsyncSession = info.context["db"]
    return await BuildingTypeService.delete(db, id)

@strawberry.type
class BuildingTypeMutation:
    create: BuildingTypeScheme = strawberry.mutation(
        resolver=create_building_type,
        description="Create a new building type",
        permission_classes=[IsAuthenticated],
    )

    update: BuildingTypeScheme = strawberry.mutation(
        resolver=update_building_type,
        description="Update an existing building type",
        permission_classes=[IsAuthenticated],
    )

    delete: bool = strawberry.mutation(
        resolver=delete_building_type,
        description="Delete a building type by its ID",
        permission_classes=[IsAuthenticated],
    )

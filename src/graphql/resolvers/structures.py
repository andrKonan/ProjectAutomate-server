# src/graphql/resolvers/structures.py
from typing import Sequence
from uuid import UUID

import strawberry
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.services import StructureTypeService
from src.graphql.schemas import StructureTypeScheme
from src.graphql.inputs import StructureTypeInput
from src.graphql.permissions import IsAuthenticated


async def get_structure_type_by_id(info: Info, id: UUID) -> StructureTypeScheme:
    db: AsyncSession = info.context["db"]
    return await StructureTypeService.get_by_id(db, id)

async def list_structure_types(info: Info) -> Sequence[StructureTypeScheme]:
    db: AsyncSession = info.context["db"]
    return await StructureTypeService.list_all(db)

@strawberry.type
class StructureTypeQuery:
    by_id: StructureTypeScheme = strawberry.field(
        resolver=get_structure_type_by_id,
        description="Fetch a single structure type by its ID",
        permission_classes=[IsAuthenticated],
    )

    all: Sequence[StructureTypeScheme] = strawberry.field(
        resolver=list_structure_types,
        description="List all structure types",
        permission_classes=[IsAuthenticated],
    )


async def create_structure_type(info: Info, input: StructureTypeInput) -> StructureTypeScheme:
    db: AsyncSession = info.context["db"]
    return await StructureTypeService.create(db, input)

async def update_structure_type(
    info: Info, id: UUID, input: StructureTypeInput
) -> StructureTypeScheme:
    db: AsyncSession = info.context["db"]
    return await StructureTypeService.update(db, id, input)

async def delete_structure_type(info: Info, id: UUID) -> bool:
    db: AsyncSession = info.context["db"]
    return await StructureTypeService.delete(db, id)

@strawberry.type
class StructureTypeMutation:
    create: StructureTypeScheme = strawberry.mutation(
        resolver=create_structure_type,
        description="Create a new structure type",
    )

    update: StructureTypeScheme = strawberry.mutation(
        resolver=update_structure_type,
        description="Update an existing structure type",
        permission_classes=[IsAuthenticated],
    )

    delete: bool = strawberry.mutation(
        resolver=delete_structure_type,
        description="Delete a structure type by its ID",
        permission_classes=[IsAuthenticated],
    )
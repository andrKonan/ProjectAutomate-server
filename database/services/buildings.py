# server/database/services/buildings.py
from typing import Sequence, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import strawberry

from server.database.models import BuildingType as BuildingTypeModel
from server.graphql.inputs import BuildingTypeInput
from server.graphql.scalars import UUID

class BuildingTypeService:
    @staticmethod
    async def get_by_id(db: AsyncSession, building_type_id: UUID) -> BuildingTypeModel:
        building_type = await db.get(BuildingTypeModel, building_type_id)
        if not building_type:
            raise HTTPException(status_code=404, detail="BuildingType not found")
        return building_type

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> Optional[BuildingTypeModel]:
        stmt = select(BuildingTypeModel).where(BuildingTypeModel.name == name)
        return (await db.execute(stmt)).scalar_one_or_none()

    @staticmethod
    async def list_all(db: AsyncSession) -> Sequence[BuildingTypeModel]:
        result = await db.execute(select(BuildingTypeModel))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, data: BuildingTypeInput) -> BuildingTypeModel:
        if await BuildingTypeService.get_by_name(db, data.name) is not None:
            raise HTTPException(status_code=403, detail="BuildingType with that name already exists")

        building_type = BuildingTypeModel(name=data.name, health=data.health)
        db.add(building_type)
        await db.commit()
        await db.refresh(building_type)
        return building_type

    @staticmethod
    async def update(db: AsyncSession, building_type_id: UUID, data: BuildingTypeInput) -> BuildingTypeModel:
        building_type = await BuildingTypeService.get_by_id(db, building_type_id)

        if data.name is not strawberry.UNSET and data.name is not None:
            building_type.name = data.name
        if data.health is not strawberry.UNSET:
            building_type.health = data.health

        await db.commit()
        await db.refresh(building_type)
        return building_type

    @staticmethod
    async def delete(db: AsyncSession, building_type_id: UUID) -> bool:
        building_type = await BuildingTypeService.get_by_id(db, building_type_id)
        await db.delete(building_type)
        await db.commit()
        return True

    @staticmethod
    async def upsert_from_dict(db: AsyncSession, data: dict) -> Optional[BuildingTypeModel]:
        if await BuildingTypeService.get_by_name(db, data.get("name", "")) is not None:
            return None

        instance = BuildingTypeModel(**data)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

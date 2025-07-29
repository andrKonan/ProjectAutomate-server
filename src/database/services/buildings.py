# server/src/database/services/buildings.py
from typing import Sequence, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import strawberry

from src.database.models import BuildingType as BuildingTypeModel, BuildingRecipe as BuildingRecipeModel
from src.database.services import ItemTypeService
from src.graphql.inputs import BuildingTypeInput
from src.graphql.scalars import UUID
from src.database import eager_load_all

class BuildingTypeService:
    @staticmethod
    async def get_by_id(db: AsyncSession, building_type_id: UUID) -> BuildingTypeModel:
        stmt = select(BuildingTypeModel).where(BuildingTypeModel.id == building_type_id).options(*eager_load_all(BuildingTypeModel, depth=2))
        result = await db.execute(stmt)
        building_type = result.scalar_one_or_none()
        if not building_type:
            raise HTTPException(status_code=404, detail="BuildingType not found")
        return building_type

    @staticmethod
    async def get_by_name(db: AsyncSession, building_type_name: str) -> Optional[BuildingTypeModel]:
        stmt = select(BuildingTypeModel).where(BuildingTypeModel.name == building_type_name).options(*eager_load_all(BuildingTypeModel, depth=2))
        building_type = await db.execute(stmt)
        return building_type.scalar_one_or_none()

    @staticmethod
    async def list_all(db: AsyncSession) -> Sequence[BuildingTypeModel]:
        result = await db.execute(select(BuildingTypeModel).options(*eager_load_all(BuildingTypeModel, depth=2)))
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
    async def create_with_recipes(db: AsyncSession, data: BuildingTypeInput) -> BuildingTypeModel:
        building_type = await BuildingTypeService.create(db, data)

        if data.building_recipes:
            for recipe in data.building_recipes:
                db.add(
                    BuildingRecipeModel(
                        building_type_id=building_type.id,
                        item_type_id=recipe.item_type_id,
                        amount=recipe.amount
                    )
                )
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
        building_type = await BuildingTypeService.get_by_name(db, data.get("name", ""))
        if building_type:
            return None

        building_type = BuildingTypeModel(name=data["name"], health=data["health"])
        db.add(building_type)
        await db.commit()
        await db.refresh(building_type)

        for recipe in data.get("recipes", []):
            item_type = await ItemTypeService.get_by_name(db, recipe["item_type"])
            if item_type is None:
                raise RuntimeError(f'ItemType "{recipe["item_type"]}" not found')

            db.add(
                BuildingRecipeModel(
                    building_type_id=building_type.id,
                    item_type_id=item_type.id,
                    amount=recipe["amount"],
                )
            )

        await db.commit()
        return building_type

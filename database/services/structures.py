# server/database/services/structures.py
from typing import Sequence, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import strawberry

from server.database.models import StructureType as StructureTypeModel
from server.graphql.schemas import StructureTypeInput

class StructureTypeService:
    @staticmethod
    async def get_by_id(db: AsyncSession, structuretype_id: str) -> StructureTypeModel:
        structuretype = await db.get(StructureTypeModel, structuretype_id)
        if not structuretype:
            raise HTTPException(status_code=404, detail="StructureType not found")
        return structuretype
    
    @staticmethod
    async def get_by_name(db: AsyncSession, structuretype_name: str) -> Optional[StructureTypeModel]:
        stmt = select(StructureTypeModel).where(StructureTypeModel.name == structuretype_name)
        return (await db.execute(stmt)).scalar_one_or_none()

    @staticmethod
    async def list_all(db: AsyncSession) -> Sequence[StructureTypeModel]:
        result = await db.execute(select(StructureTypeModel))
        return result.scalars().all()
    
    @staticmethod
    async def create(db: AsyncSession, data: StructureTypeInput) -> StructureTypeModel:
        structuretype = StructureTypeModel(
            name=data.name, 
            health=data.health,
            item_type_id=data.item_type_id,
            max_items=data.max_items,
            item_to_engage_id=data.item_to_engage_id
        )
        db.add(structuretype)
        await db.commit()
        await db.refresh(structuretype)
        return structuretype
    
    @staticmethod
    async def update(
        db: AsyncSession, structuretype_id: str, data: StructureTypeInput
    ) -> StructureTypeModel:
        structuretype = await StructureTypeService.get_by_id(db, structuretype_id)

        if data.name is not strawberry.UNSET and data.name is not None: 
            structuretype.name = data.name
            
        if data.health is not strawberry.UNSET and data.health is not None: 
            structuretype.health = data.health
        
        if data.item_type_id is not strawberry.UNSET and data.item_type_id is not None: 
            structuretype.item_type_id = data.item_type_id
            
        if data.max_items is not strawberry.UNSET and data.max_items is not None: 
            structuretype.max_items = data.max_items
        
        if data.item_to_engage_id is not strawberry.UNSET and data.item_to_engage_id is not None: 
            structuretype.item_to_engage_id = data.item_to_engage_id

        await db.commit()
        
        await db.refresh(structuretype)
        return structuretype

    @staticmethod
    async def delete(db: AsyncSession, structuretype_id: str) -> bool:
        structuretype = await StructureTypeService.get_by_id(db, structuretype_id)
        await db.delete(structuretype)
        await db.commit()
        return True
    
    @staticmethod
    async def upsert_from_dict(db: AsyncSession, data: dict) -> Optional[StructureTypeModel]:
        if await StructureTypeService.get_by_name(db, data.get("name", "")) is not None:
            return None

        instance = StructureTypeModel(**data)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance
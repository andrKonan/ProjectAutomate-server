# server/database/services/items.py
from typing import Sequence, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import strawberry

from server.database.models import ItemType as ItemTypeModel
from server.graphql.schemas import ItemTypeInput
from server.graphql.scalars import UUID

class ItemTypeService:
    @staticmethod
    async def get_by_id(db: AsyncSession, item_type_id: UUID) -> ItemTypeModel:
        itemtype = await db.get(ItemTypeModel, item_type_id)
        if not itemtype:
            raise HTTPException(status_code=404, detail="ItemType not found")
        return itemtype
    
    @staticmethod
    async def get_by_name(db: AsyncSession, itemtype_name: str) -> Optional[ItemTypeModel]:
        stmt = select(ItemTypeModel).where(ItemTypeModel.name == itemtype_name)
        return (await db.execute(stmt)).scalar_one_or_none()

    @staticmethod
    async def list_all(db: AsyncSession) -> Sequence[ItemTypeModel]:
        result = await db.execute(select(ItemTypeModel))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, data: ItemTypeInput) -> ItemTypeModel:
        itemtype = ItemTypeModel(name=data.name, durability=data.durability)
        db.add(itemtype)
        await db.commit()
        await db.refresh(itemtype)
        return itemtype

    @staticmethod
    async def update(
        db: AsyncSession, item_type_id: UUID, data: ItemTypeInput
    ) -> ItemTypeModel:
        itemtype = await ItemTypeService.get_by_id(db, item_type_id)

        if data.name is not strawberry.UNSET and data.name is not None: 
            itemtype.name = data.name
        if data.durability is not strawberry.UNSET:        # sent (may be None)
            itemtype.durability = data.durability

        await db.commit()
        
        await db.refresh(itemtype)
        return itemtype

    @staticmethod
    async def delete(db: AsyncSession, item_type_id: UUID) -> bool:
        itemtype = await ItemTypeService.get_by_id(db, item_type_id)
        await db.delete(itemtype)
        await db.commit()
        return True
    
    @staticmethod
    async def upsert_from_dict(db: AsyncSession, data: dict) -> Optional[ItemTypeModel]:
        if await ItemTypeService.get_by_name(db, data.get("name", "")) is not None:
            return None
        
        instance = ItemTypeModel(**data)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance
# server/services/items.py
import secrets
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import strawberry

from server.models import ItemType as ItemTypeModel
from server.graphql.schemas.items import ItemTypeInput

class ItemTypeService:
    @staticmethod
    async def get_by_id(db: AsyncSession, client_id: str) -> ItemTypeModel:
        client = await db.get(ItemTypeModel, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="ItemType not found")
        return client

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
        db: AsyncSession, itemtype_id: str, data: ItemTypeInput
    ) -> ItemTypeModel:
        itemtype = await ItemTypeService.get_by_id(db, itemtype_id)

        if data.name is not strawberry.UNSET and data.name is not None: 
            itemtype.name = data.name
        if data.durability is not strawberry.UNSET:        # sent (may be None)
            itemtype.durability = data.durability

        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            raise HTTPException(
                409, "Another ItemType with that name already exists"
            ) from exc
        
        await db.refresh(itemtype)
        return itemtype

    @staticmethod
    async def delete(db: AsyncSession, itemtype_id: str) -> bool:
        itemtype = await ItemTypeService.get_by_id(db, itemtype_id)
        await db.delete(itemtype)
        await db.commit()
        return True
    
    @staticmethod
    async def upsert_from_dict(db: AsyncSession, data: dict) -> ItemTypeModel:
        """
        Insert the row if it doesn't exist, otherwise do nothing.
        Works on both SQLite and Postgres.
        """
        instance = ItemTypeModel(**data)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance
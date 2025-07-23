# server/database/services/bots.py
from typing import Sequence, Optional

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
import strawberry

from server.database.models import BotType as BotTypeModel, BotRecipe as BotRecipeModel
from server.graphql.schemas import BotTypeInput
from server.graphql.scalars import UUID
from server.database import eager_load_all

class BotRecipeService:
    @staticmethod
    async def get_by_id(db: AsyncSession, bot_recipe_id: UUID) -> BotRecipeModel:
        recipe = await db.get(BotRecipeModel, bot_recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="BotRecipe not found")
        return recipe

    @staticmethod
    async def get_by_bot_type_id(db: AsyncSession, bot_type_id: UUID) -> Sequence[BotRecipeModel]:
        result = await db.execute(
            select(BotRecipeModel).where(BotRecipeModel.bot_type_id == bot_type_id)
        )
        return result.scalars().all()

    @staticmethod
    async def list_all(db: AsyncSession) -> Sequence[BotRecipeModel]:
        result = await db.execute(select(BotRecipeModel))
        return result.scalars().all()

    @staticmethod
    async def create(
        db: AsyncSession, bot_type_id: UUID, item_type_id: UUID, amount: int
    ) -> BotRecipeModel:
        recipe = BotRecipeModel(
            bot_type_id=bot_type_id,
            item_type_id=item_type_id,
            amount=amount,
        )
        db.add(recipe)
        await db.commit()
        await db.refresh(recipe)
        return recipe

    @staticmethod
    async def update(
        db: AsyncSession, recipe_id: UUID, item_type_id: Optional[int] = None, amount: Optional[int] = None
    ) -> BotRecipeModel:
        recipe = await BotRecipeService.get_by_id(db, recipe_id)

        if item_type_id is not None:
            recipe.item_type_id = item_type_id
        if amount is not None:
            recipe.amount = amount

        await db.commit()
        await db.refresh(recipe)
        return recipe

    @staticmethod
    async def delete(db: AsyncSession, recipe_id: UUID) -> bool:
        recipe = await BotRecipeService.get_by_id(db, recipe_id)
        await db.delete(recipe)
        await db.commit()
        return True

    @staticmethod
    async def upsert_from_dict(db: AsyncSession, data: dict) -> Optional[BotRecipeModel]:
        recipe = BotRecipeModel(**data)
        db.add(recipe)
        await db.commit()
        await db.refresh(recipe)
        return recipe

class BotTypeService:
    @staticmethod
    async def get_by_id(db: AsyncSession, bot_type_id: UUID) -> BotTypeModel:
        stmt = select(BotTypeModel).where(BotTypeModel.id == bot_type_id).options(*eager_load_all(BotTypeModel, depth=2))
        result = await db.execute(stmt)
        bottype = result.scalar_one_or_none()
        if not bottype:
            raise HTTPException(status_code=404, detail="BotType not found")
        return bottype
    
    @staticmethod
    async def get_by_name(db: AsyncSession, bottype_name: str) -> Optional[BotTypeModel]:
        stmt = select(BotTypeModel).where(BotTypeModel.name == bottype_name).options(*eager_load_all(BotTypeModel, depth=2))
        bottype = await db.execute(stmt)
        return bottype.scalar_one_or_none()

    @staticmethod
    async def list_all(db: AsyncSession) -> Sequence[BotTypeModel]:
        result = await db.execute(select(BotTypeModel).options(*eager_load_all(BotTypeModel, depth=2)))
        return result.scalars().all()
    
    @staticmethod
    async def create(db: AsyncSession, data: BotTypeInput) -> BotTypeModel:
        bottype = BotTypeModel(
            name=data.name,
            health=data.health,
            strength=data.strength,
            speed=data.speed,
            vision=data.vision,
        )
        db.add(bottype)
        await db.flush()

        for recipe in data.bot_recipes or []:
            db.add(
                BotRecipeModel(
                    bot_type_id=bottype.id,
                    item_id=recipe.item_type_id,
                    amount=recipe.amount,
                )
            )

        db.add(bottype)
        await db.commit()
        await db.refresh(bottype)
        return bottype
    
    @staticmethod
    async def update(
        db: AsyncSession, bottype_id: UUID, data: BotTypeInput
    ) -> BotTypeModel:
        bottype = await BotTypeService.get_by_id(db, bottype_id)

        if data.name is not strawberry.UNSET and data.name is not None:
            bottype.name = data.name

        if data.health is not strawberry.UNSET and data.health is not None:
            bottype.health = data.health

        if data.strength is not strawberry.UNSET and data.strength is not None:
            bottype.strength = data.strength

        if data.speed is not strawberry.UNSET and data.speed is not None:
            bottype.speed = data.speed

        if data.vision is not strawberry.UNSET and data.vision is not None:
            bottype.vision = data.vision

        if data.bot_recipes is not strawberry.UNSET:
            await db.execute(
                delete(BotRecipeModel).where(BotRecipeModel.bot_type_id == bottype.id)
            )
            for recipe in data.bot_recipes or []:
                db.add(
                    BotRecipeModel(
                        bot_type_id=bottype.id,
                        item_id=recipe.item_type_id,
                        amount=recipe.amount,
                    )
                )

        await db.commit()
        
        await db.refresh(bottype)
        return bottype

    @staticmethod
    async def delete(db: AsyncSession, bottype_id: UUID) -> bool:
        bottype = await BotTypeService.get_by_id(db, bottype_id)
        await db.delete(bottype)
        await db.commit()
        return True
    
    @staticmethod
    async def upsert_from_dict(db: AsyncSession, data: dict) -> Optional[BotTypeModel]:
        if await BotTypeService.get_by_name(db, data.get("name", "")) is not None:
            return None

        instance = BotTypeModel(**data)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance
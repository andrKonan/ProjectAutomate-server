# server/src/database/services/recipes.py
from typing import Sequence, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import strawberry

from src.database.models import Recipe as RecipeModel, RecipeIngredient as RecipeIngredientModel
from src.database.services import ItemTypeService
from src.graphql.inputs import RecipeInput
from src.graphql.scalars import UUID
from src.database import eager_load_all


class RecipeService:
    @staticmethod
    async def get_by_id(db: AsyncSession, recipe_id: UUID) -> RecipeModel:
        stmt = select(RecipeModel).where(RecipeModel.id == recipe_id).options(*eager_load_all(RecipeModel, depth=2))
        result = await db.execute(stmt)
        recipe = result.scalar_one_or_none()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return recipe

    @staticmethod
    async def get_by_name(db: AsyncSession, recipe_name: str) -> Optional[RecipeModel]:
        stmt = select(RecipeModel).where(RecipeModel.name == recipe_name).options(*eager_load_all(RecipeModel, depth=2))
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def list_all(db: AsyncSession) -> Sequence[RecipeModel]:
        result = await db.execute(select(RecipeModel).options(*eager_load_all(RecipeModel, depth=2)))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, data: RecipeInput) -> RecipeModel:
        if await RecipeService.get_by_name(db, data.name) is not None:
            raise HTTPException(status_code=403, detail="Recipe with that name already exists")

        recipe = RecipeModel(
            name=data.name,
            building_type_id=data.building_type_id,
            output_item_type_id=data.output_item_type_id,
            output_amount=data.output_amount
        )
        db.add(recipe)
        await db.commit()
        await db.refresh(recipe)

        if data.ingredients:
            for ingredient in data.ingredients:
                db.add(RecipeIngredientModel(
                    recipe_id=recipe.id,
                    item_type_id=ingredient.item_type_id,
                    amount=ingredient.amount
                ))

        await db.commit()
        await db.refresh(recipe)
        return recipe

    @staticmethod
    async def update(db: AsyncSession, recipe_id: UUID, data: RecipeInput) -> RecipeModel:
        recipe = await RecipeService.get_by_id(db, recipe_id)

        if data.name is not strawberry.UNSET:
            recipe.name = data.name
        if data.building_type_id is not strawberry.UNSET:
            recipe.building_type_id = data.building_type_id
        if data.output_item_type_id is not strawberry.UNSET:
            recipe.output_item_type_id = data.output_item_type_id
        if data.output_amount is not strawberry.UNSET:
            recipe.output_amount = data.output_amount

        # Replace ingredients
        if data.ingredients is not strawberry.UNSET and data.ingredients is not None:
            recipe.ingredients.clear()
            for ingredient in data.ingredients:
                recipe.ingredients.append(RecipeIngredientModel(
                    item_type_id=ingredient.item_type_id,
                    amount=ingredient.amount
                ))

        await db.commit()
        await db.refresh(recipe)
        return recipe

    @staticmethod
    async def delete(db: AsyncSession, recipe_id: UUID) -> bool:
        recipe = await RecipeService.get_by_id(db, recipe_id)
        await db.delete(recipe)
        await db.commit()
        return True

    @staticmethod
    async def upsert_from_dict(db: AsyncSession, data: dict) -> Optional[RecipeModel]:
        recipe = await RecipeService.get_by_name(db, data["name"])
        if recipe:
            return None

        recipe = RecipeModel(
            name=data["name"],
            building_type_id=data["building_type_id"],
            output_item_type_id=data["output_item_type_id"],
            output_amount=data["output_amount"]
        )
        db.add(recipe)
        await db.commit()
        await db.refresh(recipe)

        for ing in data.get("ingredients", []):
            item_type = await ItemTypeService.get_by_name(db, ing["item_type"])
            if item_type is None:
                raise RuntimeError(f'ItemType "{ing["item_type"]}" not found')

            db.add(RecipeIngredientModel(
                recipe_id=recipe.id,
                item_type_id=item_type.id,
                amount=ing["amount"]
            ))

        await db.commit()
        return recipe
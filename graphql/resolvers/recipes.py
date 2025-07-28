# server/graphql/resolvers/recipes.py
from typing import Sequence
from uuid import UUID

import strawberry
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession

from server.database.services import RecipeService
from server.graphql.schemas.recipes import RecipeScheme
from server.graphql.inputs.recipes import RecipeInput
from server.graphql.permissions import IsAuthenticated


async def get_recipe_by_id(info: Info, id: UUID) -> RecipeScheme:
    db: AsyncSession = info.context["db"]
    return await RecipeService.get_by_id(db, id)

async def list_recipes(info: Info) -> Sequence[RecipeScheme]:
    db: AsyncSession = info.context["db"]
    return await RecipeService.list_all(db)


@strawberry.type
class RecipeQuery:
    by_id: RecipeScheme = strawberry.field(
        resolver=get_recipe_by_id,
        description="Fetch a single recipe by its ID",
        permission_classes=[IsAuthenticated],
    )

    all: Sequence[RecipeScheme] = strawberry.field(
        resolver=list_recipes,
        description="List all recipes",
        permission_classes=[IsAuthenticated],
    )


async def create_recipe(info: Info, input: RecipeInput) -> RecipeScheme:
    db: AsyncSession = info.context["db"]
    return await RecipeService.create(db, input)

async def update_recipe(info: Info, id: UUID, input: RecipeInput) -> RecipeScheme:
    db: AsyncSession = info.context["db"]
    return await RecipeService.update(db, id, input)

async def delete_recipe(info: Info, id: UUID) -> bool:
    db: AsyncSession = info.context["db"]
    return await RecipeService.delete(db, id)


@strawberry.type
class RecipeMutation:
    create: RecipeScheme = strawberry.mutation(
        resolver=create_recipe,
        description="Create a new recipe",
        permission_classes=[IsAuthenticated],
    )

    update: RecipeScheme = strawberry.mutation(
        resolver=update_recipe,
        description="Update an existing recipe",
        permission_classes=[IsAuthenticated],
    )

    delete: bool = strawberry.mutation(
        resolver=delete_recipe,
        description="Delete a recipe by its ID",
        permission_classes=[IsAuthenticated],
    )
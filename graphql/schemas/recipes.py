# server/graphql/schemas/recipes.py
from datetime import datetime

import strawberry

from server.graphql.scalars import UUID

@strawberry.type(description="A RecipeIngredient in the system")
class RecipeIngredientScheme:
    id: UUID
    recipe_id: UUID
    item_type_id: UUID
    amount: int
    created_at: datetime

@strawberry.type(description="A Recipe in the system")
class RecipeScheme:
    id: UUID
    name: str
    building_type_id: UUID
    output_item_type_id: UUID
    output_amount: int
    ingredients: list[RecipeIngredientScheme] | None
    created_at: datetime

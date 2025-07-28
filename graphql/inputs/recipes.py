# server/graphql/inputs/recipes.py
import strawberry

from server.graphql.scalars import UUID

@strawberry.input(description="Payload for creating/updating a RecipeIngredient")
class RecipeIngredientInput:
    item_type_id: UUID
    amount: int

@strawberry.input(description="Payload for creating/updating a Recipe")
class RecipeInput:
    name: str
    building_type_id: UUID
    output_item_type_id: UUID
    output_amount: int
    ingredients: list[RecipeIngredientInput] | None
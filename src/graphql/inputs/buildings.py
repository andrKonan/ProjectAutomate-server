# server/src/graphql/inputs/buildings.py
import strawberry

from src.graphql.scalars import UUID

@strawberry.input(description="Payload for creating/updating a BuildingRecipe")
class BuildingRecipeInput:
    building_type_id: UUID
    item_type_id: UUID
    amount: int

@strawberry.input(description="Payload for creating/updating a BuildingType")
class BuildingTypeInput:
    name: str
    health: int
    building_recipes: list[BuildingRecipeInput] | None
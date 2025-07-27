# server/graphql/schemas/buildings.py
from datetime import datetime

import strawberry

from server.graphql.scalars import UUID

@strawberry.type(description="A BuildingRecipe in the system")
class BuildingRecipeScheme:
    id: UUID
    building_type_id: UUID
    item_type_id: UUID
    amount: int
    created_at: datetime

@strawberry.type(description="Payload for creating/updating a BuildingType")
class BuildingTypeScheme:
    id: UUID
    name: str
    health: int
    building_recipes: list[BuildingRecipeScheme] | None
    created_at: datetime
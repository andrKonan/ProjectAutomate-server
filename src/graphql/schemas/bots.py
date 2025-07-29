# server/src/graphql/schemas/bots.py
from datetime import datetime

import strawberry

from src.graphql.scalars import UUID

@strawberry.type(description="A BotRecipe in the system")
class BotRecipeScheme:
    id: UUID
    bot_type_id: UUID
    item_type_id: UUID
    amount: UUID
    created_at: datetime


@strawberry.type(description="A BotType in the system")
class BotTypeScheme:
    id: UUID
    name: str
    health: int
    strength: int
    speed: int
    vision: int
    bot_recipes: list[BotRecipeScheme]
    created_at: datetime

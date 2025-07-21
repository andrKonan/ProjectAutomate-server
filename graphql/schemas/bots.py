# server/graphql/schema/clients.py
from datetime import datetime

import strawberry

from server.graphql.scalars import UUID

@strawberry.type(description="A BotRecipe in the system")
class BotRecipeScheme:
    id: UUID
    bot_type_id: UUID
    item_type_id: UUID
    amount: UUID
    created_at: datetime

@strawberry.input(description="Payload for creating/updating a BotRecipe")
class BotRecipeInput:
    bot_type_id: UUID
    item_type_id: UUID
    amount: UUID


@strawberry.type(description="A BotType in the system")
class BotTypeScheme:
    id: UUID
    name: str
    health: int
    strength: int
    speed: int
    vision: int
    recipes: list[BotRecipeScheme]
    created_at: datetime

@strawberry.input(description="Payload for creating/updating a BotType")
class BotTypeInput:
    name: str
    health: int
    strength: int
    speed: int
    vision: int
    recipes: list[BotRecipeScheme] | None = None


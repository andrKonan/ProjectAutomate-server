# src/graphql/inputs/bots.py
import strawberry

from src.graphql.scalars import UUID

@strawberry.input(description="Payload for creating/updating a BotRecipe")
class BotRecipeInput:
    bot_type_id: UUID
    item_type_id: UUID
    amount: UUID

@strawberry.input(description="Payload for creating/updating a BotType")
class BotTypeInput:
    name: str
    health: int
    strength: int
    speed: int
    vision: int
    bot_recipes: list[BotRecipeInput] | None = None
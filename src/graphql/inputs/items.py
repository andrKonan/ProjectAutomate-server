# src/graphql/inputs/items.py
import strawberry

@strawberry.input(description="Payload for creating/updating a ItemType")
class ItemTypeInput:
    name: str
    durability: int | None
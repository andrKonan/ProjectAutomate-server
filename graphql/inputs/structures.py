# server/graphql/inputs/structures.py
import strawberry

from server.graphql.scalars import UUID

@strawberry.input(description="Payload for creating/updating a StructureType")
class StructureTypeInput:
    name: str
    health: int
    item_type_id: UUID
    max_items: int
    item_to_engage_id: UUID | None
# server/graphql/schema/items.py
from datetime import datetime

import strawberry

from server.graphql.scalars import UUID

@strawberry.type(description="An ItemType in the system")
class ItemTypeScheme:
    id: UUID
    name: str
    durability: int | None
    created_at: datetime

@strawberry.input(description="Payload for creating/updating a ItemType")
class ItemTypeInput:
    name: str
    durability: int | None

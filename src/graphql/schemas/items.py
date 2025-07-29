# server/src/graphql/schemas/items.py
from datetime import datetime

import strawberry

from src.graphql.scalars import UUID

@strawberry.type(description="An ItemType in the system")
class ItemTypeScheme:
    id: UUID
    name: str
    durability: int | None
    created_at: datetime



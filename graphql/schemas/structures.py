# server/graphql/schema/structures.py
from datetime import datetime

import strawberry

from server.graphql.scalars import UUID

@strawberry.type(description="A StructureType in the system")
class StructureTypeScheme:
    id: UUID
    name: str
    health: int
    item_type_id: UUID
    max_items: int
    item_to_engage_id: UUID | None
    created_at: datetime


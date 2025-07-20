# server/schema/items.py
from datetime import datetime

import strawberry

@strawberry.type(description="A customer/client in the system")
class ItemTypeScheme:
    id: strawberry.ID
    name: str
    durability: int | None
    created_at: datetime

@strawberry.input(description="Payload for creating/updating a Client")
class ItemTypeInput:
    name: str
    durability: int | None

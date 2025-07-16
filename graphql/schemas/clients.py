# server/schema/clients.py
from datetime import datetime

import strawberry

@strawberry.type(description="A customer/client in the system")
class ClientType:
    id: strawberry.ID
    name: str
    _token: str
    created_at: datetime

@strawberry.input(description="Payload for creating/updating a Client")
class ClientInput:
    name: str

# server/graphql/schema/clients.py
from datetime import datetime

import strawberry

from server.graphql.scalars import UUID

@strawberry.type(description="A customer/client in the system")
class ClientScheme:
    id: UUID
    name: str
    _token: str
    created_at: datetime

@strawberry.input(description="Payload for creating/updating a Client")
class ClientInput:
    name: str

# server/graphql/inputs/clients.py
from uuid import UUID

import strawberry

@strawberry.input(description="Payload for creating a Client")
class ClientCreateInput:
    name: str

@strawberry.input(description="Payload for updating a Client")
class ClientUpdateInput:
    id: UUID
    name: str

# src/graphql/inputs/clients.py
import strawberry

from src.graphql.scalars import UUID

@strawberry.input(description="Payload for creating a Client")
class ClientCreateInput:
    name: str

@strawberry.input(description="Payload for updating a Client")
class ClientUpdateInput:
    id: UUID
    name: str

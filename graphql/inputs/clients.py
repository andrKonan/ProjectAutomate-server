# server/graphql/inputs/clients.py
import strawberry

@strawberry.input(description="Payload for creating/updating a Client")
class ClientInput:
    name: str
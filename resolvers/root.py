# server/schema/root.py
import strawberry

from .clients import ClientQuery, ClientMutation

@strawberry.type
class Query(ClientQuery):
    pass

@strawberry.type
class Mutation(ClientMutation):
    pass

# server/schema/root.py
import strawberry

from server.graphql.resolvers.clients import ClientQuery, ClientMutation
from server.graphql.resolvers.items import ItemTypeQuery, ItemTypeMutation

@strawberry.type
class Query(
        ClientQuery, 
        ItemTypeQuery
    ):
    pass

@strawberry.type
class Mutation(
        ClientMutation, 
        ItemTypeMutation
    ):
    pass

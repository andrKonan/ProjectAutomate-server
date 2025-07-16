# server/schema/root.py
import strawberry

from server.graphql.resolvers.clients import ClientQuery, ClientMutation

@strawberry.type
class Query(ClientQuery):
    pass

@strawberry.type
class Mutation(ClientMutation):
    pass

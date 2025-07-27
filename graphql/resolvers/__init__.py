# server/graphql/resolvers/__init__.py
import strawberry

from .clients import ClientQuery, ClientMutation
from .items import ItemTypeQuery, ItemTypeMutation
from .structures import StructureTypeQuery, StructureTypeMutation
from .bots import BotTypeQuery, BotTypeMutation

@strawberry.type
class Query():
    client: ClientQuery = strawberry.field(resolver=ClientQuery)
    item_type: ItemTypeQuery = strawberry.field(resolver=ItemTypeQuery)
    structure_type: StructureTypeQuery = strawberry.field(resolver=StructureTypeQuery)
    bot_type: BotTypeQuery = strawberry.field(resolver=BotTypeQuery)

@strawberry.type
class Mutation():
    client: ClientMutation = strawberry.mutation(resolver=ClientMutation)
    item_type: ItemTypeMutation = strawberry.mutation(resolver=ItemTypeMutation)
    structure_type: StructureTypeMutation = strawberry.mutation(resolver=StructureTypeMutation)
    bot_type: BotTypeMutation = strawberry.field(resolver=BotTypeMutation)

__all__ = [
    "Query", "Mutation"
]
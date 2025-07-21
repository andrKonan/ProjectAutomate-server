# server/graphql/schema/root.py
import strawberry

from .clients import ClientQuery, ClientMutation
from .items import ItemTypeQuery, ItemTypeMutation
from .structures import StructureTypeQuery, StructureTypeMutation

@strawberry.type
class Query():
    client: ClientQuery = strawberry.field(resolver=ClientQuery)
    item_type: ItemTypeQuery = strawberry.field(resolver=ItemTypeQuery)
    structure_type: StructureTypeQuery = strawberry.field(resolver=StructureTypeQuery)

@strawberry.type
class Mutation():
    client: ClientMutation = strawberry.mutation(resolver=ClientMutation)
    item_type: ItemTypeMutation = strawberry.mutation(resolver=ItemTypeMutation)
    structure_type: StructureTypeMutation = strawberry.mutation(resolver=StructureTypeMutation)

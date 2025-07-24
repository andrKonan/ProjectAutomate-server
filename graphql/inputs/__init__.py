# server/graphql/inputs/__init__.py
from .clients import ClientCreateInput, ClientUpdateInput
from .items import ItemTypeInput
from .structures import StructureTypeInput
from .bots import BotRecipeInput, BotTypeInput

__all__ = [
    "ClientCreateInput", "ClientUpdateInput",
    "ItemTypeInput",
    "StructureTypeInput",
    "BotRecipeInput", "BotTypeInput"
]
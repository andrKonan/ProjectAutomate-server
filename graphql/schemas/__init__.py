# server/graphql/schemas/__init__.py
from .clients import ClientScheme, ClientInput
from .items import ItemTypeScheme, ItemTypeInput
from .structures import StructureTypeScheme, StructureTypeInput
from .bots import BotRecipeScheme, BotRecipeInput, BotTypeScheme, BotTypeInput

__all__ = [
    "ClientScheme", "ClientInput",
    "ItemTypeScheme", "ItemTypeInput",
    "StructureTypeScheme", "StructureTypeInput",
    "BotRecipeScheme", "BotRecipeInput", "BotTypeScheme", "BotTypeInput"
]
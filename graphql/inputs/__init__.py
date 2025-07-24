# server/graphql/inputs/__init__.py
from .clients import ClientInput
from .items import ItemTypeInput
from .structures import StructureTypeInput
from .bots import BotRecipeInput, BotTypeInput

__all__ = [
    "ClientInput",
    "ItemTypeInput",
    "StructureTypeInput",
    "BotRecipeInput", "BotTypeInput"
]
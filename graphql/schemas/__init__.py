# server/graphql/schemas/__init__.py
from .clients import ClientScheme
from .items import ItemTypeScheme
from .structures import StructureTypeScheme
from .bots import BotRecipeScheme, BotTypeScheme

__all__ = [
    "ClientScheme",
    "ItemTypeScheme",
    "StructureTypeScheme",
    "BotRecipeScheme", "BotTypeScheme",
]
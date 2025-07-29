# src/graphql/schemas/__init__.py
from .clients import ClientScheme
from .items import ItemTypeScheme
from .structures import StructureTypeScheme
from .bots import BotRecipeScheme, BotTypeScheme
from .buildings import BuildingRecipeScheme, BuildingTypeScheme
from .recipes import RecipeIngredientScheme, RecipeScheme

__all__ = [
    "ClientScheme",
    "ItemTypeScheme",
    "StructureTypeScheme",
    "BotRecipeScheme", "BotTypeScheme",
    "BuildingRecipeScheme", "BuildingTypeScheme",
    "RecipeIngredientScheme", "RecipeScheme"
]
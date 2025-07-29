# src/graphql/inputs/__init__.py
from .clients import ClientCreateInput, ClientUpdateInput
from .items import ItemTypeInput
from .structures import StructureTypeInput
from .bots import BotRecipeInput, BotTypeInput
from .buildings import BuildingRecipeInput, BuildingTypeInput
from .recipes import RecipeIngredientInput, RecipeInput

__all__ = [
    "ClientCreateInput", "ClientUpdateInput",
    "ItemTypeInput",
    "StructureTypeInput",
    "BotRecipeInput", "BotTypeInput",
    "BuildingRecipeInput", "BuildingTypeInput",
    "RecipeIngredientInput", "RecipeInput"
]
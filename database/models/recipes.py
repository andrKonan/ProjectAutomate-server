# server/database/models/recipes.py
from __future__ import annotations

from uuid import UUID

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseRepr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.items import ItemType

class RecipeIngredient(BaseRepr):
    __tablename__ = "recipe_ingredients"

    item_type_id:   Mapped[int] = mapped_column(ForeignKey("item_types.id"))
    amount:    Mapped[int] = mapped_column(Integer)
    recipe_id: Mapped[UUID] = mapped_column(ForeignKey("recipes.id"))

    item_type: Mapped["ItemType"] = relationship("ItemType")


class Recipe(BaseRepr):
    __tablename__ = "recipes"

    name: Mapped[str] = mapped_column(String, unique=True)

    building_type_id:    Mapped[int] = mapped_column(ForeignKey("building_types.id"))
    output_item_type_id: Mapped[UUID] = mapped_column(ForeignKey("item_types.id"))
    output_amount:       Mapped[int] = mapped_column(Integer)

    ingredients:   Mapped[list["RecipeIngredient"]] = relationship(
        "RecipeIngredient", cascade="all, delete-orphan"
    )
    output_item_type: Mapped["ItemType"]  = relationship("ItemType")
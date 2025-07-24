# server/database/models/buildings.py
from __future__ import annotations

from uuid import UUID

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseRepr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .items import ItemType
    from .recipes import Recipe
    from .clients import Client

class BuildingRecipe(BaseRepr):
    __tablename__ = "building_recipes"

    building_type_id: Mapped[UUID] = mapped_column(ForeignKey("building_types.id"))
    item_type_id: Mapped[UUID] = mapped_column(ForeignKey("item_types.id"))
    amount: Mapped[int] = mapped_column(Integer)

    item_type: Mapped["ItemType"] = relationship("ItemType")

class BuildingType(BaseRepr):
    __tablename__ = "building_types"

    name: Mapped[str] = mapped_column(String, unique=True)

    health: Mapped[int] = mapped_column(Integer)

    building_recipes: Mapped[list["BuildingRecipe"]] = relationship("BuildingRecipe")
    recipes:          Mapped[list["Recipe"]] = relationship("Recipe")

class Building(BaseRepr):
    __tablename__ = "buildings"

    name:      Mapped[str] = mapped_column(String, default="Unnamed Building")
    type_id:   Mapped[int] = mapped_column(ForeignKey("building_types.id"))
    client_id: Mapped[UUID] = mapped_column(ForeignKey("clients.id"))

    x: Mapped[int] = mapped_column(Integer)
    y: Mapped[int] = mapped_column(Integer)

    level: Mapped[int] = mapped_column(Integer)
    current_health: Mapped[int] = mapped_column(Integer)

    type: Mapped["BuildingType"] = relationship("BuildingType")
    client: Mapped["Client"] = relationship("Client")

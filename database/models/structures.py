# server/database/models/structures.py
from __future__ import annotations

from uuid import UUID

from sqlalchemy_utils import UUIDType
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseRepr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .items import ItemType

class StructureType(BaseRepr):
    __tablename__ = "structure_types"

    name: Mapped[str] = mapped_column(String, unique=True)
    health: Mapped[int] = mapped_column(Integer)
    item_type_id: Mapped[UUID] = mapped_column(
        UUIDType(binary=True),
        ForeignKey("item_types.id"),
        nullable=False,
    )
    max_items: Mapped[int] = mapped_column(Integer)
    item_to_engage_id: Mapped[UUID] = mapped_column(
        UUIDType(binary=True),
        ForeignKey("item_types.id"), 
        nullable=True
    )

    # Specify which FK to use for each relationship
    item_type: Mapped["ItemType"] = relationship(
        "ItemType",
        foreign_keys=[item_type_id]
    )
    item_to_engage: Mapped["ItemType"] = relationship(
        "ItemType",
        foreign_keys=[item_to_engage_id]
    )

class Structure(BaseRepr):
    __tablename__ = "structures"

    type_id: Mapped[UUID] = mapped_column(
        UUIDType(binary=True),
        ForeignKey("structure_types.id")
    )
    items: Mapped[int] = mapped_column(Integer, default=0)
    x: Mapped[int] = mapped_column(Integer)
    y: Mapped[int] = mapped_column(Integer)

    type: Mapped[StructureType] = relationship("StructureType")
# server/models/items.py
from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseRepr


class ItemType(BaseRepr):
    __tablename__ = "item_types"

    name: Mapped[str] = mapped_column(String, unique=True)
    durability: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)

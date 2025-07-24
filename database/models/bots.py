# server/database/models/bots.py
from __future__ import annotations

from uuid import UUID

from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseRepr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .items import ItemType
    from .clients import Client


class BotRecipe(BaseRepr):
    __tablename__ = "bot_recipes"

    bot_type_id: Mapped[UUID] = mapped_column(ForeignKey("bot_types.id"))
    item_type_id:     Mapped[int] = mapped_column(ForeignKey("item_types.id"))
    amount:      Mapped[int] = mapped_column(Integer)

    item_type: Mapped["ItemType"] = relationship("ItemType")


class BotType(BaseRepr):
    __tablename__ = "bot_types"

    name: Mapped[str] = mapped_column(String, unique=True)

    health:   Mapped[int] = mapped_column(Integer)
    strength: Mapped[int] = mapped_column(Integer)
    speed:    Mapped[int] = mapped_column(Integer)
    vision:   Mapped[int] = mapped_column(Integer)

    bot_recipes: Mapped[list["BotRecipe"]] = relationship("BotRecipe")


class BotInventorySlot(BaseRepr):
    __tablename__ = "bot_inventory_slots"

    bot_id: Mapped[UUID] = mapped_column(ForeignKey("bots.id"))
    slot_index: Mapped[int] = mapped_column(Integer)  # 0-based slot index
    item_id: Mapped[int | None] = mapped_column(ForeignKey("item_types.id"), nullable=True)
    item_durability: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)

    item: Mapped["ItemType"] = relationship("ItemType")

    __table_args__ = (
        UniqueConstraint("bot_id", "slot_index", name="uq_bot_slot"),
    )


class Bot(BaseRepr):
    __tablename__ = "bots"

    name:      Mapped[str] = mapped_column(String, default="Unnamed Bot")
    type_id:   Mapped[int] = mapped_column(ForeignKey("bot_types.id"))
    client_id: Mapped[UUID] = mapped_column(ForeignKey("clients.id"))

    x: Mapped[int] = mapped_column(Integer)
    y: Mapped[int] = mapped_column(Integer)

    level: Mapped[int] = mapped_column(Integer, default=1)

    type:   Mapped["BotType"] = relationship("BotType")
    client: Mapped["Client"]  = relationship("Client")

    inventory: Mapped[list["BotInventorySlot"]] = relationship(
        "BotInventorySlot", cascade="all, delete-orphan"
    )

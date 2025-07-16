# server/models/base.py
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy_utils import UUIDType

Base = declarative_base()

class BaseRepr(Base):
    """Colourful `repr()` that skips SQLAlchemy internals."""
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        UUIDType(binary=True), 
        primary_key=True, 
        default=uuid.uuid4
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        res = f"<\033[94m{self.__class__.__name__}\033[0m("
        for k, v in self.__dict__.items():
            if k.startswith("_"):
                continue
            if isinstance(v, Enum):
                v = v.name
            elif isinstance(v, datetime):
                v = v.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(v, BaseRepr):
                v = repr(v)
            res += f"\033[92m{k}\033[0m=\033[93m{v!r}\033[0m, "
        return res.rstrip(", ") + ")>"
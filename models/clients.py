# server/models/clients.py
from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseRepr


class Client(BaseRepr):
    __tablename__ = "clients"

    name: Mapped[str]       = mapped_column(String,  unique=True)
    _token: Mapped[str]     = mapped_column(String,  unique=True, index=True)

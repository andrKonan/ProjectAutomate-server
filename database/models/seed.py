# server/database/models/seed.py
from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseRepr

class SeedMeta(BaseRepr):
    """
    Records the SHA-256 hash of each seed file that has been applied.
    Pure ORM ⇒ no raw SQL anywhere.
    """
    __tablename__ = "seed_meta"

    file_sha: Mapped[str] = mapped_column(String)
    file_path: Mapped[str] = mapped_column(String)

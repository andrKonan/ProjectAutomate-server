# src/graphql/scalars.py
import uuid
from typing import Annotated

import strawberry

UuidScalar = strawberry.scalar(
    uuid.UUID,
    serialize=lambda v: str(v),
    parse_value=uuid.UUID,
    description="RFC-4122 UUID",
)

# Type alias that *is* a real typing construct
UUID = Annotated[uuid.UUID, UuidScalar]
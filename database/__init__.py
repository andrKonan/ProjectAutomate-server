# server/database/__init__.py
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from server.config import settings

engine = create_async_engine(settings.db_url, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db()-> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session



from sqlalchemy.orm import selectinload, class_mapper

def eager_load_all(model, depth=2):
    opts = []
    if depth <= 0:
        return opts
    for rel in class_mapper(model).relationships:
        loader = selectinload(getattr(model, rel.key))
        sub_opts = eager_load_all(rel.mapper.class_, depth=depth-1)
        if sub_opts:
            loader = loader.options(*sub_opts)
        opts.append(loader)
    return opts
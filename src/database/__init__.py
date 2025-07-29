# server/src/database/__init__.py
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config import get_settings

_engine = None
def get_engine():
    global _engine
    if _engine is None:
        _engine = create_async_engine(get_settings().db_url, echo=False, future=True)
    return _engine

_session = None
def get_sessionmaker():
    global _session
    if _session is None:
        _session = async_sessionmaker(get_engine(), expire_on_commit=False)
    return _session

async def get_db()-> AsyncGenerator[AsyncSession, None]:
    session_local = get_sessionmaker()
    async with session_local() as session:
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
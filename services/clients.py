# server/services/clients.py
import secrets
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Client as ClientModel
from ..schemas.clients import ClientInput

class ClientService:
    @staticmethod
    async def get_by_id(db: AsyncSession, client_id: str) -> ClientModel:
        client = await db.get(ClientModel, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client

    @staticmethod
    async def get_by_token(db: AsyncSession, token: str) -> ClientModel:
        stmt = select(ClientModel).where(ClientModel._token == token)
        
        result = await db.execute(stmt)
        
        return result.scalar_one_or_none()


    @staticmethod
    async def list_all(db: AsyncSession) -> Sequence[ClientModel]:
        result = await db.execute(select(ClientModel))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, data: ClientInput) -> ClientModel:
        token = secrets.token_hex(64)
        client = ClientModel(name=data.name, _token=token)
        db.add(client)
        await db.commit()
        await db.refresh(client)
        return client

    @staticmethod
    async def update(
        db: AsyncSession, client_id: str, data: ClientInput
    ) -> ClientModel:
        # Client can't be updated
        client = await ClientService.get_by_id(db, client_id)
        return client

    @staticmethod
    async def delete(db: AsyncSession, client_id: str) -> bool:
        client = await ClientService.get_by_id(db, client_id)
        await db.delete(client)
        await db.commit()
        return True
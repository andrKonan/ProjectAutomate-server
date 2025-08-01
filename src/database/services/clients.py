# src/database/services/clients.py
import secrets
from typing import Sequence, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Client as ClientModel
from src.graphql.inputs import ClientCreateInput, ClientUpdateInput
from src.graphql.scalars import UUID

class ClientService:
    @staticmethod
    async def get_by_id(db: AsyncSession, client_id: UUID) -> ClientModel:
        client = await db.get(ClientModel, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client

    @staticmethod
    async def get_by_token(db: AsyncSession, token: str) -> Optional[ClientModel]:
        stmt = select(ClientModel).where(ClientModel._token == token)
        
        result = await db.execute(stmt)
        
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> Optional[ClientModel]:
        stmt = select(ClientModel).where(ClientModel.name == name)

        result = await db.execute(stmt)

        return result.scalar_one_or_none()
    
    @staticmethod
    async def list_all(db: AsyncSession) -> Sequence[ClientModel]:
        result = await db.execute(select(ClientModel))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, data: ClientCreateInput) -> ClientModel:
        client = await ClientService.get_by_name(db, data.name)
        if client is not None:
            raise HTTPException(status_code=403, detail="Client with that name already exists")
        
        token = secrets.token_hex(64)
        client = ClientModel(name=data.name, _token=token)
        db.add(client)
        await db.commit()
        await db.refresh(client)
        return client

    @staticmethod
    async def update(
        db: AsyncSession, data: ClientUpdateInput
    ) -> ClientModel:
        client = await ClientService.get_by_id(db, data.id)
        
        if client is not None:
            client.name = data.name

        await db.commit()
        await db.refresh(client)

        return client

    @staticmethod
    async def delete(db: AsyncSession, client_id: UUID) -> bool:
        client = await ClientService.get_by_id(db, client_id)
        await db.delete(client)
        await db.commit()
        return True
from loguru import logger
from typing import TypeVar, List
from sqlalchemy.ext.asyncio import AsyncSession
from taskbot.dao.base import BaseDAO
from taskbot.dao.schemas import BaseModel
from taskbot.dao.session_maker import connection

class BaseService():
    dao: type[BaseDAO]

    @classmethod
    @connection
    async def find_all(cls, session: AsyncSession, filters: BaseModel = None):
        records = await cls.dao.find_all(session, filters)

        return records
    
    @classmethod
    @connection
    async def find_by_ids(cls, session: AsyncSession, ids: List[int]):
        records = await cls.dao.find_by_ids(session, ids)
        
        return records
    
    @classmethod
    @connection
    async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel):
        record = await cls.dao.find_one_or_none(session, filters)

        return record
    
    @classmethod
    @connection
    async def find_one_or_none_by_id(cls, session: AsyncSession, data_id: int):
        record = await cls.dao.find_one_or_none_by_id(session, data_id)

        return record
    
    @classmethod
    @connection
    async def add(cls, session: AsyncSession, values: BaseModel):
        record = await cls.dao.add(session, values)
        await session.commit()

        return record
    
    @classmethod
    @connection
    async def delete(cls, session: AsyncSession, filters: BaseModel):
        record = await cls.dao.delete(session, filters)
        await session.commit()

        return record

    @classmethod
    @connection
    async def count(cls, session: AsyncSession, filters: BaseModel):
        return await cls.dao.count(session, filters)

    @classmethod
    @connection
    async def paginate(cls, session: AsyncSession, page: int = 1, page_size: int = 10, filters: BaseModel = None):
        return await cls.dao.paginate(session, page, page_size, filters)

    @classmethod
    @connection
    async def upsert(cls, session: AsyncSession, unique_fields: List[str], values: BaseModel):
        return cls.dao.upsert(session,unique_fields, values)

    @classmethod
    @connection
    async def bulk_update(cls, session: AsyncSession, records: List[BaseModel]):
        return await cls.dao.bulk_update(session, records)

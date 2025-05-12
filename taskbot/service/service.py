from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from taskbot.dao.dao import RoleDAO
from taskbot.dao.session_maker import connection

class RoleService():
    dao: RoleDAO

    def __init__(self, dao: RoleDAO):
        self.dao = dao

    @connection
    async def find_one_or_none_by_id(session: AsyncSession):
        role = await RoleDAO.find_one_or_none_by_id(session, id)

        return role

    @connection
    async def find_one_or_none(session: AsyncSession, filters: BaseModel):
        role = await RoleDAO.find_one_or_none(session, filters)

        return role

from loguru import logger
from typing import List
from aiogram.filters import BaseFilter
from aiogram.types import Message 
from sqlalchemy.ext.asyncio import AsyncSession
from taskbot.dao.dao import UserDAO
from taskbot.admin.schemas import UserTelegramAndRoleIds
from taskbot.dao.session_maker import connection

class IsAdmin(BaseFilter):
    def __init__(self, expected: bool = True):
        self.expected = expected

    @connection    
    async def __call__(self, message: Message, session: AsyncSession):
        id = message.from_user.id
        user = await UserDAO.find_one_or_none(
            session,
            UserTelegramAndRoleIds(
                telegram_id=id,
                role_id=1
            )
        )
        
        isAdminOrNotText = 'admin' if user else 'not admin'
        logger.info(f"user#{id} is {isAdminOrNotText}")

        return (user != None) == self.expected

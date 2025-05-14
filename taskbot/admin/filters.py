from loguru import logger
from typing import List
from aiogram.filters import BaseFilter
from aiogram.types import Message 
from sqlalchemy.ext.asyncio import AsyncSession
from taskbot.dao.dao import UserDAO
from taskbot.admin.schemas import UserTelegramAndRoleIds

class IsAdmin(BaseFilter):
    def __init__(self, user_ids: int | List[int]):
        self.user_ids = user_ids

    async def __call__(self, message: Message, session_without_commit: AsyncSession):
        id = message.from_user.id
        user = await UserDAO.find_one_or_none(
            session_without_commit,
            UserTelegramAndRoleIds(
                telegram_id=id,
                role_id=1
            )
        )
        
        return user != None
        if isinstance(self.user_ids, int):
            return id == self.user_ids
        return id in self.user_ids
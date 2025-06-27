from loguru import logger
from typing import List
from aiogram.filters import BaseFilter
from aiogram.types import Message 
from sqlalchemy.ext.asyncio import AsyncSession
from taskbot.dao.dao import UserDAO
from taskbot.admin.schemas import UserTelegramId
from taskbot.dao.session_maker import connection


class IsAdmin(BaseFilter):
    def __init__(self, expected: bool = True):
        self.expected = expected

    @connection    
    async def __call__(self, message: Message, session: AsyncSession, *args, **kwargs):
        id = message.from_user.id
        user = await UserDAO.find_one_or_none(
            session,
            UserTelegramId(
                telegram_id=id
            )
        )
        
        if user is None:
            logger.info(f"user#{id} не зарегистрирован")
            await message.answer(
                'У вас нет доступа так как вы не зарегистрированны. Для регистрации введите команду <b>/start</b>',
                reply_markup=None
            )
            return False
        else:
            isAdmin = user.role_id == 1

        isAdminOrNotText = 'администратор' if isAdmin else 'не администратор'
        logger.info(f"user#{id} - {isAdminOrNotText}")

        return isAdmin == self.expected

class PassUsersWithRoleIds(BaseFilter):
    def __init__(self, roleIds: List[int]):
        self.expectedRoleIds = roleIds

    @connection
    async def __call__(self, message: Message, session: AsyncSession, *args, **kwargs):
        user = await UserDAO.find_one_or_none(
            session,
            UserTelegramId(
                    telegram_id=message.from_user.id
                )
            )

        try:
            self.expectedRoleIds.index(user.role_id)
        except Exception as e:
            return False
        
        return True

class FilterUserByRoles(BaseFilter):
    def __init__(self, roles: List[str]):
        self.expectedRoles = roles

    @connection
    async def __call__(self, message: Message, session: AsyncSession, *args, **kwargs):
        user = await UserDAO.find_one_or_none(
            session,
            UserTelegramId(
                    telegram_id=message.from_user.id
                )
            )

        try:
            self.expectedRoleIds.index(user.role_id)
        except Exception as e:
            return False
        
        return True


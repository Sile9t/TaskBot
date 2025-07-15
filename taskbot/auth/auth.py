from loguru import logger
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy import select
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from ..dao.database import async_session_maker
from ..dao.models import User
from ..dao.dao import UserDAO, RoleDAO
from ..dao.filters import FilterUserByTelegramId
from ..admin.schemas import UserTelegramId


class AuthenticateMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ):
        if (event.message is None):
            message = event.callback_query
        else:
            message = event.message
        telegramId = message.from_user.id
        
        if (telegramId is not None):
            async with async_session_maker() as session:
                user = await UserDAO.find_one_or_none(
                    session,
                    FilterUserByTelegramId(
                        telegram_id=telegramId
                    )
                )
                
                if (user is None):

                    newUser = User()
                    newUser.first_name = message.from_user.first_name
                    newUser.last_name = message.from_user.last_name
                    newUser.telegram_id = message.from_user.id
                    role_id = 3

                    count = await UserDAO.count(session)
                    if (count == 0):
                        role_id = 1
                    newUser.role_id = role_id
                    query = session.add(newUser)
                    await session.commit()
            
            if (user is None):
                async with async_session_maker() as session:
                    user = await UserDAO.find_one_or_none(
                        session,
                        FilterUserByTelegramId(
                            telegram_id=telegramId
                        )
                    )    

            data['auth'] = user
        await handler(event, data)

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from taskbot.dao.database import async_session_maker
from taskbot.dao.dao import UserDAO
from taskbot.admin.schemas import UserTelegramId

class AuthenticateMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ):
        async with async_session_maker() as session:
            userId = event.message.from_user.id
            user = await UserDAO.find_one_or_none(
                session,
                UserTelegramId(telegram_id=userId)
            )

        data['auth'] = user
        await handler(event, data)
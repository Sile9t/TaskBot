from loguru import logger
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy import select
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from ..dao.database import async_session_maker
from ..dao.models import User
from ..dao.dao import UserDAO
from ..admin.schemas import UserTelegramId

class AuthenticateMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ):
        if (event.callback_query is not None):
            userId = event.callback_query.from_user.id
        elif (event.message is not None):
            userId = event.message.from_user.id
        
        if (userId is not None):
            async with async_session_maker() as session:
                query = select(User).filter_by(telegram_id=userId)
                result = await session.execute(query)
                user = result.unique().scalar_one_or_none()

            data['auth'] = user
        await handler(event, data)
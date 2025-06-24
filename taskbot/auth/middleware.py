from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import BaseMiddleware
from aiogram.types import Message

class AuthMiddleware(BaseMiddleware):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event, data):
        user_tg_id = handler.message.user_from.id
        return await super().__call__(handler, event, data)
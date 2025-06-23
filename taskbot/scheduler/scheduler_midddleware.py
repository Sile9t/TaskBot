from typing import Any, Dict, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from .scheduler import TaskNotifier

class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        data["apscheduler"] = self.scheduler
        return await handler(event, data)

class NotifierMiddleware(BaseMiddleware):
    def __init__(self, notifier: TaskNotifier):
        self.notifier = notifier

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        data["notifier"] = self.notifier
        return await handler(event, data)
    

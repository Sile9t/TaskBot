from loguru import logger
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from taskbot.admin.kbs import main_admin_kb
from taskbot.dao.dao import UserDAO
from taskbot.dao.models import User
from taskbot.admin.schemas import UserTelegramId
from taskbot.admin.filters import IsAdmin


admin_router = Router()
admin_router.message.filter(IsAdmin())


@admin_router.message(Command('admin_panel'))
async def admin_panel(message: Message, session_without_commit: AsyncSession, auth: User|None):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов команды admin/admin_panel")

    if (auth.role_id == 1):
        return await message.answer(
            text=f"Выберите необходимое действие:",
            reply_markup=main_admin_kb(auth.role_id)
        )
    
    await message.answer(
        text=f"У вас нет доступа к админ-панели!",
        reply_markup=None
    )


@admin_router.callback_query(F.data == "admin_panel")
async def admin_panel(call: CallbackQuery, session_without_commit: AsyncSession, auth: User):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/admin_panel")
    
    if (auth.role_id == 1):
        await call.answer("Доступ в админ-панель разрешен!")
        return await call.message.edit_text(
            text=f"Выберите необходимое действие:",
            reply_markup=main_admin_kb(auth.role_id)
        )

    await call.message.edit_text(
        text=f"У вас нет доступа к админ-панели!",
        reply_markup=None
    )

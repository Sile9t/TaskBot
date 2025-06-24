import asyncio
from loguru import logger
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from taskbot.role.state import RoleCreate, RoleRead, RoleUpdate, RoleDelete
from taskbot.role.kbs import role_menu_kb
from ..admin.filters import IsAdmin

role_router = Router()
role_router.message.filter(IsAdmin())

@role_router.message(Command('role_menu'))
async def role_menu(message: Message):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов кнопки admin/role_menu")
    await message.answer(
        text=f"Меню должностей:",
        reply_markup=role_menu_kb()
    )


@role_router.callback_query(F.data == 'role_menu')
async def role_menu(call: CallbackQuery):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/role_menu")
    await call.message.edit_text(
        text=f"Меню должностей:",
        reply_markup=role_menu_kb()
    )


@role_router.message(F.text.startswith("role_list"))
@role_router.callback_query(F.data.startswith("role_list"))
async def role_list(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/role_list")

    await call.answer()
    await dialog_manager.start(
        state=RoleRead.id,
        mode=StartMode.RESET_STACK
    )


@role_router.callback_query(F.data == "role_add")
async def role_add(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/role_add\nЗапуск сценария добавления должности")

    await call.answer("Добавление должности")
    await dialog_manager.start(
        state=RoleCreate.name,
        mode=StartMode.RESET_STACK
    )


@role_router.callback_query(F.data == "role_update")
async def role_update(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/role_update")

    await call.answer("Изменение должности")
    await dialog_manager.start(
        state=RoleUpdate.id,
        mode=StartMode.RESET_STACK
    )


@role_router.callback_query(F.data == "role_delete")
async def role_delete(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}:Вызов сценария удаления должности")

    await call.answer("Удаление должности")
    await dialog_manager.start(
        state=RoleDelete.id,
        mode=StartMode.RESET_STACK
    )

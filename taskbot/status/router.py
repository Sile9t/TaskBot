from loguru import logger
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from taskbot.status.state import StatusCreate, StatusRead, StatusUpdate, StatusDelete
from taskbot.status.kbs import status_menu_kb

from ..admin.filters import PassUsersWithRoleIds


status_router = Router()
status_router.message.filter(PassUsersWithRoleIds([1, 2]))


@status_router.message(Command('status_menu'))
async def status_menu(message: Message):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов кнопки admin/status_menu")
    await message.answer(
        text=f"Меню для статусов:",
        reply_markup=status_menu_kb()
    )


@status_router.callback_query(F.data == 'status_menu')
async def status_menu(call: CallbackQuery):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/status_menu")
    await call.message.edit_text(
        text=f"Меню для статусов:",
        reply_markup=status_menu_kb()
    )


@status_router.message(F.text.startswith("status_list"))
@status_router.callback_query(F.data.startswith("status_list"))
async def status_list(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/status_list")

    await call.answer()
    await dialog_manager.start(
        state=StatusRead.id,
        mode=StartMode.RESET_STACK
    )


@status_router.callback_query(F.data == "status_add")
async def status_add(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/status_add\nЗапуск сценария добавления записи статуса")

    await call.answer("Добавление записи статуса")
    await dialog_manager.start(
        state=StatusCreate.title,
        mode=StartMode.RESET_STACK
    )


@status_router.callback_query(F.data == "status_update")
async def status_update(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/status_update")

    await call.answer("Изменение записи статуса")
    await dialog_manager.start(
        state=StatusUpdate.id,
        mode=StartMode.RESET_STACK
    )


@status_router.callback_query(F.data == "status_delete")
async def status_delete(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов сценария удаления записи статуса")

    await call.answer("Удаление записи статуса")
    await dialog_manager.start(
        state=StatusDelete.id,
        mode=StartMode.RESET_STACK
    )

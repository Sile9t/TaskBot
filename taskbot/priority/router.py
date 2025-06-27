from loguru import logger
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from taskbot.priority.state import PriorityCreate, PriorityRead, PriorityUpdate, PriorityDelete
from taskbot.priority.kbs import priority_menu_kb
from ..admin.filters import PassUsersWithRoleIds

priority_router = Router()
priority_router.message.filter(PassUsersWithRoleIds([1, 2]))


@priority_router.message(Command('priority_menu'))
async def priority_menu(message: Message):
    logger.info(f"chat#{message.chat.id}|user#{message.from_user.id}: Вызов кнопки admin/priority_menu")
    await message.answer(
        text=f"Меню для приоритетов:",
        reply_markup=priority_menu_kb()
    )


@priority_router.callback_query(F.data == 'priority_menu')
async def priority_menu(call: CallbackQuery):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/priority_menu")
    await call.message.edit_text(
        text=f"Меню для приоритетов:",
        reply_markup=priority_menu_kb()
    )


@priority_router.message(F.text.startswith("priority_list"))
@priority_router.callback_query(F.data.startswith("priority_list"))
async def priority_list(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/priority_list")

    await call.answer()
    await dialog_manager.start(
        state=PriorityRead.id,
        mode=StartMode.RESET_STACK
    )


@priority_router.callback_query(F.data == "priority_add")
async def priority_add(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/priority_add\nЗапуск сценария добавления записи приоритета")

    await call.answer("Добавление записи приоритета")
    await dialog_manager.start(
        state=PriorityCreate.value,
        mode=StartMode.RESET_STACK
    )


@priority_router.callback_query(F.data == "priority_update")
async def priority_update(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов кнопки admin/priority_update")

    await call.answer("Изменение записи приоритета")
    await dialog_manager.start(
        state=PriorityUpdate.id,
        mode=StartMode.RESET_STACK
    )


@priority_router.callback_query(F.data == "priority_delete")
async def priority_delete(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Вызов сценария удаления записи приоритета")

    await call.answer("Удаление записи приоритета")
    await dialog_manager.start(
        state=PriorityDelete.id,
        mode=StartMode.RESET_STACK
    )

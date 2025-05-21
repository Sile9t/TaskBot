import asyncio
from typing import Dict, Any
from loguru import logger
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender
from aiogram_dialog import DialogManager, StartMode
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from taskbot.dao.dao import RoleDAO
from taskbot.dao.schemas import RoleDtoBase, RoleDto
from taskbot.admin.kbs import yes_no_kb, pass_kb, role_menu_kb, role_list_kb
from taskbot.admin.utils import extract_number
from taskbot.role.state import FormCreate, FormRead, FormUpdate, FormRemove

role_router = Router()

@role_router.message(Command("cancel"))
@role_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.info("Сброс состояния %r", current_state)
    await state.clear()
    await message.answer(
        "Отменено.",
        reply_markup=ReplyKeyboardRemove(),
    )


@role_router.message(Command('role_menu'))
async def role_menu(message: Message):
    logger.info("Вызов кнопки admin/role_menu")
    await message.answer(
        text=f"Меню должностей:",
        reply_markup=role_menu_kb()
    )


@role_router.callback_query(F.data == 'role_menu')
async def role_menu(call: CallbackQuery):
    logger.info("Вызов кнопки admin/role_menu")
    await call.message.edit_text(
        text=f"Меню должностей:",
        reply_markup=role_menu_kb()
    )


@role_router.message(F.text.startswith("role_list"))
@role_router.callback_query(F.data.startswith("role_list"))
async def role_list(call: CallbackQuery, session_without_commit: AsyncSession, dialog_manager: DialogManager):
    logger.info("Вызов кнопки admin/role_list")

    await call.answer()
    
    await dialog_manager.start(
        state=FormRead.id,
        mode=StartMode.RESET_STACK
    )


@role_router.callback_query(F.data == "role_add")
async def role_add(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"Вызов кнопки admin/role_add\nЗапуск сценария добавления должности")

    await call.answer("Добавление должности")
    await dialog_manager.start(
        state=FormCreate.name,
        mode=StartMode.RESET_STACK
    )


@role_router.callback_query(F.data == "role_update")
async def role_update(call: CallbackQuery, state: FSMContext, session_with_commit: AsyncSession, dialog_manager: DialogManager):
    logger.info("Вызов кнопки admin/role_update")

    await call.answer("Изменение должности")
    await dialog_manager.start(
        state=FormUpdate.id,
        mode=StartMode.RESET_STACK
    )


@role_router.callback_query(F.data == "role_delete")
async def role_delete(call: CallbackQuery, state: FSMContext, session_with_commit: AsyncSession, dialog_manager: DialogManager):
    logger.info("Вызов сценария удаления должности")

    await call.answer("Удаление должности")
    await dialog_manager.start(
        state=FormRemove.id,
        mode=StartMode.RESET_STACK
    )

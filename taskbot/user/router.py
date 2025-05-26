import asyncio
from loguru import logger
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from taskbot.user.state import UserCreate, UserRead, UserUpdate, UserDelete
from taskbot.user.kbs import user_menu_kb

user_router = Router()

@user_router.message(Command("cancel"))
@user_router.message(F.text.casefold() == "cancel")
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


@user_router.message(Command('user_menu'))
async def user_menu(message: Message):
    logger.info("Вызов кнопки admin/user_menu")
    await message.answer(
        text=f"Меню для сотрудников:",
        reply_markup=user_menu_kb()
    )


@user_router.callback_query(F.data == 'user_menu')
async def user_menu(call: CallbackQuery):
    logger.info("Вызов кнопки admin/user_menu")
    await call.message.edit_text(
        text=f"Меню для сотрудников:",
        reply_markup=user_menu_kb()
    )


@user_router.message(F.text.startswith("user_list"))
@user_router.callback_query(F.data.startswith("user_list"))
async def user_list(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info("Вызов кнопки admin/user_list")

    await call.answer()
    await dialog_manager.start(
        state=UserRead.id,
        mode=StartMode.RESET_STACK
    )


@user_router.callback_query(F.data == "user_add")
async def user_add(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"Вызов кнопки admin/user_add\nЗапуск сценария добавления должности")

    await call.answer("Добавление должности")
    await dialog_manager.start(
        state=UserCreate.first_name,
        mode=StartMode.RESET_STACK
    )


@user_router.callback_query(F.data == "user_update")
async def user_update(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info("Вызов кнопки admin/user_update")

    await call.answer("Изменение должности")
    await dialog_manager.start(
        state=UserUpdate.id,
        mode=StartMode.RESET_STACK
    )


@user_router.callback_query(F.data == "user_delete")
async def user_delete(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info("Вызов сценария удаления должности")

    await call.answer("Удаление должности")
    await dialog_manager.start(
        state=UserDelete.id,
        mode=StartMode.RESET_STACK
    )

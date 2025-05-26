import asyncio
from loguru import logger
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from config import settings, bot
from taskbot.dao.dao import TaskDAO
from taskbot.dao.schemas import TaskDto
from taskbot.user.kbs import user_menu_kb
user_router = Router()

@user_router.message(Command("help"))
async def cmd_help(message: Message):
    logger.info("Вызов команды user/help")
    await message.answer(
        f"Список комманд:",
        reply_markup=None
    )
    

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    logger.info("Вызов команды user/start")
    await message.answer(
        f"👋🏻 Привет, {message.from_user.full_name}!\nВыберите дальнейшие действия:",
        reply_markup=user_menu_kb()
    )


@user_router.message(Command("cancel"))
@user_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=None,
    )


# @user_router.callback_query(F.data == "task_menu")
# async def task_menu(call: CallbackQuery):
#     logger.info("Вызов команды user/task_menu")
#     await call.message.edit_text(
#         text=f"Выберите действия с задачами:",
#         reply_markup=task_kb()
#     )

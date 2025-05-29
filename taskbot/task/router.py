import asyncio
from loguru import logger
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from taskbot.task.state import TaskCreate, TaskRead, TaskUpdate, TaskDelete
from taskbot.task.kbs import task_menu_kb

task_router = Router()

@task_router.message(Command("cancel"))
@task_router.message(F.text.casefold() == "cancel")
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


@task_router.message(Command('task_menu'))
async def task_menu(message: Message):
    logger.info("Вызов кнопки admin/task_menu")
    await message.answer(
        text=f"Меню для задач:",
        reply_markup=task_menu_kb()
    )


@task_router.callback_query(F.data == 'task_menu')
async def task_menu(call: CallbackQuery):
    logger.info("Вызов кнопки admin/task_menu")
    await call.message.edit_text(
        text=f"Меню для задач:",
        reply_markup=task_menu_kb()
    )


@task_router.message(F.text.startswith("task_list"))
@task_router.callback_query(F.data.startswith("task_list"))
async def task_list(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info("Вызов кнопки admin/task_list")

    await call.answer()
    await dialog_manager.start(
        state=TaskRead.id,
        mode=StartMode.RESET_STACK
    )


@task_router.callback_query(F.data == "task_add")
async def task_add(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"Вызов кнопки admin/task_add\nЗапуск сценария добавления задачи")

    await call.answer("Добавление задачи")
    await dialog_manager.start(
        state=TaskCreate.title,
        mode=StartMode.RESET_STACK
    )


@task_router.callback_query(F.data == "task_update")
async def task_update(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info("Вызов кнопки admin/task_update")

    await call.answer("Изменение задачи")
    await dialog_manager.start(
        state=TaskUpdate.id,
        mode=StartMode.RESET_STACK
    )


@task_router.callback_query(F.data == "task_delete")
async def task_delete(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info("Вызов сценария удаления задачи")

    await call.answer("Удаление задачи")
    await dialog_manager.start(
        state=TaskDelete.id,
        mode=StartMode.RESET_STACK
    )

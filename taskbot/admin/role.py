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
from taskbot.role.state import FormCreate, FormUpdate, FormRemove

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


async def getPagesCount(session: AsyncSession, filters: BaseModel = None):
    rolesCount = await RoleDAO.count(session, filters)
    pagesCount = rolesCount / 5
    
    return pagesCount

async def getRoleList(text: str, session: AsyncSession, filters: BaseModel = None):
    logger.info(f"getRoleList text value: {text}")
    if (text.find('role_list_') > -1):
        page = int(text.replace('role_list_', ''))
    else:
        page = 1
    logger.info(f'getRoleList page value: {page}')
    
    roles = await RoleDAO.paginate(session, page, 5, filters)
    
    pagesCount = await getPagesCount(session, filters)
    
    caption = (
        f'Список должностей:\n'
    )
    
    logger.info('Составление списка должностей')
    for role in roles:
        caption += (
            f'ID: {role.id}\n'
            f'Название: {role.name}\n'
            f'Описание: {role.description}\n'
            f'\n'
        )

    return (caption, page, pagesCount)

@role_router.message(F.text.startswith("role_list"))
async def role_list(message: Message, session_without_commit: AsyncSession):
    logger.info("Вызов команды admin/role_list")
    
    (data, page, pagesCount) = await getRoleList(message.text, session_without_commit)

    await message.edit_text(
        text=data,
        reply_markup=role_list_kb(page, pagesCount)
    )


@role_router.callback_query(F.data.startswith("role_list"))
async def role_list(call: CallbackQuery, session_without_commit: AsyncSession):
    logger.info("Вызов кнопки admin/role_list")

    await call.answer()
    (caption, page, pagesCount) = await getRoleList(call.data, session_without_commit)
    
    logger.info(f"Возврат списка должностей")
    await call.message.edit_text(
        text=caption,
        reply_markup=role_list_kb(page, pagesCount)
    )


@role_router.callback_query(F.data == "role_add")
async def role_add(call: CallbackQuery, dialog_manager: DialogManager):
    logger.info(f"Вызов кнопки admin/role_add\nЗапуск сценария добавления должности")

    await call.answer("Добавление должности")
    await dialog_manager.start(
        state=FormCreate.name,
        mode=StartMode.RESET_STACK
    )


@role_router.message(FormCreate.name)
async def capture_name(message: Message, state: FSMContext):
    logger.info("Сценарий добавления должности: захват 'name'")
    await state.update_data(name=message.text)
    
    await state.set_state(FormCreate.description)
    await message.answer(
        text="Введите описание должности (опционально):",
        reply_markup=pass_kb()
    )

@role_router.message(FormCreate.description)
async def capture_description(message: Message, state: FSMContext):
    logger.info("Сценарий добавления должности: захват 'description'")
    if (message.text.find("пропустить".casefold()) == -1):
        await state.update_data(description=None)
    else:
        await state.update_data(description=message.text)

    data = await state.get_data()
    roleText = await get_summary(data)    
    caption = f"Проверьте данные:\n\n" \
            f"{roleText}\n\n" \
            f"Все верно?"

    await state.set_state(FormCreate.confirmation)
    await message.answer(
        text=caption,
        reply_markup=yes_no_kb()
    )

async def get_summary(data: Dict[str, Any]):
    caption = f"Название: {data.get('name')}\n" \
            f"Описание: {data.get('description') if (data.get('description')) else ''}"
    
    return caption

@role_router.callback_query(F.data == 'yes', FormCreate.confirmation)
async def process_role(call: CallbackQuery, state: FSMContext, session_with_commit: AsyncSession):
    logger.info("Сценарий добавления должности: подтверждение добавления")
    data = await state.get_data()
    if (data == None):
        return await call.message.edit_text(
            text="Данные утеряны. Попробуйте выполнить сценарий заново",
            reply_markup=None
        )
    
    role = RoleDtoBase(
        name=data.get('name'),
        description=data.get('description')
    )
    role = await RoleDAO.add(session_with_commit, role)
    
    answer='Данные сохранены',
    if (role.id < 1):
        answer='Сбой при сохранении данных',
    
    await call.message.edit_text(
        text=answer,
        reply_markup=role_menu()
    )
    await state.clear()

@role_router.callback_query(F.data == 'no', FormCreate.confirmation)
async def restart_form(call: CallbackQuery, state: FSMContext):
    logger.info("Сценарий добавления должности: запуск с начала")
    
    await call.message.edit_text(
        text=f"Запуск сценария я начала.\nВведите название должности:",
        reply_markup=None
    )
    await state.set_state(FormCreate.name)


@role_router.callback_query(F.data == "role_update" & F.text)
async def role_update(call: CallbackQuery, state: FSMContext, session_with_commit: AsyncSession):
    logger.info("Вызов кнопки admin/role_update")

    (data, page, pagesCount) = await getRoleList(call.message.text, session_with_commit)
    
    data += f"\nВведите ID должности для изменения"
    logger.info(f"Возврат списка должностей")
    await state.set_state(FormRemove.Id)
    await call.message.edit_text(
        text=data,
        reply_markup=role_list_kb(page, pagesCount)
    )

@role_router.message(FormUpdate.name)
async def capture_name(message: Message, state: FSMContext):
    logger.info("Сценарий добавления должности: захват 'name'")
    await state.update_data(name=message.text)
    
    await state.set_state(FormUpdate.description)
    await message.answer(
        text="Введите описание должности (опционально):",
        reply_markup=pass_kb()
    )

@role_router.message(FormUpdate.description)
async def capture_description(message: Message, state: FSMContext):
    logger.info("Сценарий добавления должности: захват 'description'")
    if (message.text.find("пропустить".casefold()) == -1):
        await state.update_data(description=None)
    else:
        await state.update_data(description=message.text)

    data = await state.get_data()
    roleText = await get_summary(data)    
    caption = f"Проверьте данные:\n\n" \
            f"{roleText}\n\n" \
            f"Все верно?"

    await state.set_state(FormUpdate.check_state)
    await message.answer(
        text=caption,
        reply_markup=yes_no_kb()
    )


@role_router.callback_query(F.data == "role_delete")
async def role_delete(call: CallbackQuery, state: FSMContext, session_with_commit: AsyncSession):
    logger.info("Вызов сценария удаления должности")

    (data, page, pagesCount) = await getRoleList(call.message.text, session_with_commit)
    
    data += f"\nВведите ID должности для удаления"
    logger.info(f"Возврат списка должностей")
    await state.set_state(FormRemove.Id)
    await call.message.edit_text(
        text=data,
        reply_markup=role_list_kb(page, pagesCount)
    )

@role_router.message(FormRemove.Id)
async def role_delete(message: Message, state: FSMContext, session_with_commit: AsyncSession):
    logger.info("Вызов кнопки admin/role_delete")
    text = message.text

    id = extract_number(text)
    
    if (id is not None):
        role = await RoleDAO.find_one_or_none_by_id(session_with_commit, id)

        if role:
            count = await RoleDAO.delete(
                session_with_commit,
                RoleDto(
                    id=role.id,
                    name=role.name,
                    description=role.description
                )
            )
            
            text = f"Удалено {count} записей"
            await state.clear()
            return await message.answer(
                text=text,
                reply_markup=None
            )
    
    await message.answer(
        text="Должности с таким ID не существует. Введите ID заново.",
        reply_markup=None
    )

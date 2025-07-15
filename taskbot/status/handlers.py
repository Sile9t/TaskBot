from typing import Any
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from ..dao.dao import TaskStatusDAO
from ..dao.schemas import TaskStatusDtoBase
from ..admin.kbs import main_admin_kb
from ..status.kbs import status_menu_kb
from ..status.state import StatusUpdate
from ..general.schemas import FilterRecordById


async def go_menu(call: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await call.answer("Сценарий отменен!")
    await call.message.answer(
        "Вы отменили сценарий. Меню для статусов заданий:",
        reply_markup=status_menu_kb()
    )


async def on_status_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    status_id = int(item_id)
    status = await TaskStatusDAO.find_one_or_none_by_id(session, status_id)
    
    dialog_manager.dialog_data["status"] = status
    await call.answer(f"Выбрана запись №{status_id}")
    await dialog_manager.next()


async def on_status_to_delete_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    status_id = int(item_id)
    count = await TaskStatusDAO.delete(
        session, 
        FilterRecordById(
            id=status_id
        )
    )
    selected_region = await TaskStatusDAO.find_one_or_none_by_id(session, status_id)
    if (selected_region is None):
        return call.answer(f"Выбраная запись №{status_id} не существует. Выберите еще раз")

    text = f"Удалено {count} записей"
    await session.commit()
    await call.answer(text)

    await dialog_manager.done()


async def on_status_id_input_error(message: Message, dialog_: Any, dialog_manager: DialogManager, error_: ValueError, **kwargs):
    await message.answer("Номер должен быть числом!")


async def on_create_confirmation(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    session = dialog_manager.middleware_data.get("session_with_commit")

    userRoleId = auth.role_id if auth else 3
    title = dialog_manager.find("title").get_value()
    description = dialog_manager.find("description").get_value()
    newstatus = TaskStatusDtoBase(
        title=title,
        description=description
    )

    check = await TaskStatusDAO.find_one_or_none(session, newstatus)
    if not check:
        await callback.answer("Сохранение")
        await TaskStatusDAO.add(session, newstatus)
        text = "Запись статуса успешно сохранена."
        await callback.answer(text)
        await callback.message.answer(text, reply_markup=main_admin_kb(userRoleId))

        await dialog_manager.done()
    else:
        await callback.message.answer("Такая запись уже существует!")
        await dialog_manager.back()

    
async def on_update_confirmation(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    session = dialog_manager.middleware_data.get("session_with_commit")
    
    userRoleId = auth.role_id if auth else 3
    status = dialog_manager.dialog_data.get('status') 
    title = dialog_manager.find('title').get_value()
    description = dialog_manager.find('description').get_value()
    
    if status:
        await callback.answer("Сохранение")
        
        status.title = title
        status.description = description

        await session.commit()

        text = "Запись статуса успешно обновлена."
        await callback.answer(text)
        await callback.message.answer(text, reply_markup=main_admin_kb(userRoleId))

        await dialog_manager.done()


async def process_delete_status(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    session = dialog_manager.middleware_data.get("session_with_commit")

    userRoleId = auth.role_id if auth else 3
    id = dialog_manager.find("id").get_value()
    status = dialog_manager.dialog_data.get('status')
    
    if status:
        await call.answer("Удаление записи")
        statusDto = statusDto(
            id=status.id,
            title=status.title,
            description=status.description
        )
        count = await TaskStatusDAO.delete(session, statusDto)
        text = f"Удалено {count} записей"
        await session.commit()
        await call.message.answer(
            text,
            reply_markup=main_admin_kb(userRoleId)
        )
        
        await dialog_manager.done()
    
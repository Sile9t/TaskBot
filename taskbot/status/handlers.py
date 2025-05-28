from typing import Any
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from taskbot.dao.dao import TaskStatusDAO
from taskbot.dao.schemas import TaskStatusDto, TaskStatusDtoBase
from taskbot.admin.kbs import main_admin_kb
from taskbot.status.kbs import status_menu_kb
from taskbot.status.state import StatusUpdate

async def go_menu(call: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await call.answer("Сценарий отменен!")
    await call.message.answer(
        "Вы отменили сценарий. Меню для статусов заданий:",
        reply_markup=status_menu_kb()
    )

async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.answer("Сценарий отменен!")
    await callback.message.answer(
        "Вы отменили сценарий.", 
        reply_markup=main_admin_kb(callback.from_user.id)
    )


async def on_status_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str):
    session = dialog_manager.middleware_data.get("session_without_commit")
    status_id = int(item_id)
    selected_status = await TaskStatusDAO(session).find_one_or_none_by_id(status_id)

    dialog_manager.dialog_data["selected_status"] = selected_status
    await call.answer(f"Выбрана запись статуса №{status_id}")
    await dialog_manager.next()


async def on_status_id_input_error(message: Message, dialog_: Any, dialog_manager: DialogManager, error_: ValueError):
    await message.answer("Номер должен быть числом!")

{    
# async def on_status_id_input(message: Message, dialog_: Any, dialog_manager: DialogManager):
#     session = dialog_manager.middleware_data.get("session_without_commit")

#     id = dialog_manager.find('id').get_value()
#     status = await TaskStatusDAO.find_one_or_none_by_id(session, id)

#     if status is None:
#         await message.answer(f"Должности с таким номером не существует!\nВведите его еще раз.")
#         return
    
#     await dialog_manager.next()
}


async def on_create_confirmation(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")

    user_id = callback.from_user.id
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
        await callback.answer(f"Запись статуса успешно создана!")
        text = "Запись статуса успешно сохранена"
        await callback.message.answer(text, reply_markup=main_admin_kb())

        await dialog_manager.done()
    else:
        await callback.message.answer("Такая запись уже существует!")
        await dialog_manager.back()

    
async def on_update_confirmation(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")
    
    user_id = callback.from_user.id
    id = dialog_manager.find('id').get_value()
    title = dialog_manager.find('title').get_value()
    description = dialog_manager.find('description').get_value()
    
    check = await TaskStatusDAO.find_one_or_none_by_id(session, id)
    if check:
        await callback.answer("Сохранение")
        
        check.title = title
        check.description = description

        await session.commit()

        await callback.answer(f"Запись статуса успешно обновлена!")
        text = "Запись статуса успешно сохранена"
        await callback.message.answer(text, reply_markup=main_admin_kb())

        await dialog_manager.done()
    else:
        await callback.message.answer("Такая запись не существует!")
        await dialog_manager.switch_to(StatusUpdate.id)


async def process_delete_status(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")

    id = dialog_manager.find("id").get_value()
    status = await TaskStatusDAO.find_one_or_none_by_id(session, id)
    
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
        await call.answer(text)
        
        await dialog_manager.done()
    else:
        await call.answer("Такая запись статуса не существует!\nВведите другой номер.")

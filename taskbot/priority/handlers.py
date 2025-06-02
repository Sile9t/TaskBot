from typing import Any
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from taskbot.dao.dao import TaskPriorityDAO
from taskbot.dao.schemas import TaskPriorityDto, TaskPriorityDtoBase
from taskbot.admin.kbs import main_admin_kb
from taskbot.priority.kbs import priority_menu_kb
from taskbot.priority.state import PriorityUpdate

async def go_menu(call: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await call.answer("Сценарий отменен!")
    await call.message.answer(
        "Вы отменили сценарий. Меню для приоритетов заданий:",
        reply_markup=priority_menu_kb()
    )

async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.answer("Сценарий отменен!")
    await callback.message.answer(
        "Вы отменили сценарий.", 
        reply_markup=main_admin_kb(callback.from_user.id)
    )


async def on_priority_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str):
    session = dialog_manager.middleware_data.get("session_without_commit")
    priority_id = int(item_id)
    selected_priority = await TaskPriorityDAO.find_one_or_none_by_id(session, priority_id)
    if (selected_priority is None):
        return call.answer(f"Выбраная запись №{priority_id} не существует. Выберите еще раз")

    dialog_manager.dialog_data['priority_id'] = priority_id
    dialog_manager.dialog_data["selected_priority"] = selected_priority
    await call.answer(f"Выбрана запись №{priority_id}")
    await dialog_manager.next()


async def on_priority_id_input_error(message: Message, dialog_: Any, dialog_manager: DialogManager, error_: ValueError):
    await message.answer("Номер должен быть числом!")

{    
# async def on_priority_id_input(message: Message, dialog_: Any, dialog_manager: DialogManager):
#     session = dialog_manager.middleware_data.get("session_without_commit")

#     id = dialog_manager.find('id').get_value()
#     priority = await TaskPriorityDAO.find_one_or_none_by_id(session, id)

#     if priority is None:
#         await message.answer(f"Должности с таким номером не существует!\nВведите его еще раз.")
#         return
    
#     await dialog_manager.next()
}


async def on_create_confirmation(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")

    user_id = callback.from_user.id
    value = dialog_manager.find('value').get_value()
    title = dialog_manager.find("title").get_value()
    description = dialog_manager.find("description").get_value()
    newpriority = TaskPriorityDtoBase(
        value=value,
        title=title,
        description=description
    )

    check = await TaskPriorityDAO.find_one_or_none(session, newpriority)
    if not check:
        await callback.answer("Сохранение")
        await TaskPriorityDAO.add(session, newpriority)
        await callback.answer(f"Запись приоритета успешно создана!")
        text = "Запись приоритета успешно сохранена"
        await callback.message.answer(text, reply_markup=main_admin_kb())

        await dialog_manager.done()
    else:
        await callback.message.answer("Такая запись уже существует!")
        await dialog_manager.back()

    
async def on_update_confirmation(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")
    
    user_id = callback.from_user.id
    id = dialog_manager.find('id').get_value()
    value = dialog_manager.find('value').get_value()
    title = dialog_manager.find('title').get_value()
    description = dialog_manager.find('description').get_value()
    
    check = await TaskPriorityDAO.find_one_or_none_by_id(session, id)
    if check:
        await callback.answer("Сохранение")
        
        check.value = value
        check.title = title
        check.description = description

        await session.commit()

        await callback.answer(f"Запись приоритета успешно обновлена!")
        text = "Запись приоритета успешно сохранена"
        await callback.message.answer(text, reply_markup=main_admin_kb())

        await dialog_manager.done()
    else:
        await callback.message.answer("Такая запись не существует!")
        await dialog_manager.switch_to(PriorityUpdate.id)


async def process_delete_priority(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")

    id = dialog_manager.find("id").get_value()
    priority = await TaskPriorityDAO.find_one_or_none_by_id(session, id)
    
    if priority:
        await call.answer("Удаление записи")
        priorityDto = TaskPriorityDto(
            id=priority.id,
            value=priority.value,
            title=priority.title,
            description=priority.description
        )
        count = await TaskPriorityDAO.delete(session, priorityDto)
        text = f"Удалено {count} записей"
        await session.commit()
        await call.answer(text)
        
        await dialog_manager.done()
    else:
        await call.answer("Такая запись приоритета не существует!\nВведите другой номер.")

from typing import Any
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from taskbot.dao.dao import RoleDAO
from taskbot.dao.schemas import RoleDto, RoleDtoBase
from taskbot.admin.kbs import main_admin_kb
from taskbot.role.kbs import role_menu_kb
from taskbot.role.state import RoleUpdate

async def go_menu(call: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await call.answer("Сценарий отменен!")
    await call.message.answer(
        "Вы отменили сценарий. Меню для должностей:",
        reply_markup=role_menu_kb()
    )

async def on_role_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str):
    session = dialog_manager.middleware_data.get("session_without_commit")
    role_id = int(item_id)
    selected_role = await RoleDAO.find_one_or_none_by_id(session, role_id)
    if (selected_role is None):
        return call.answer(f"Выбраная запись №{role_id} не существует. Выберите еще раз")

    dialog_manager.dialog_data["role"] = selected_role
    await call.answer(f"Выбрана должность №{role_id}")
    await dialog_manager.next()

async def on_role_delete_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str):
    session = dialog_manager.middleware_data.get("session_without_commit")
    role_id = int(item_id)
    role = await RoleDAO.find_one_or_none_by_id(session, role_id)
    if (role is None):
        return call.message.answer(f"Выбраная запись №{role_id} не существует. Выберите еще раз")

    dialog_manager.dialog_data["role"] = role

    roleDto = RoleDto(
        id=role.id,
        name=role.name,
        description=role.description
    )
    count = await RoleDAO.delete(session, roleDto)
    text = f"Удалено {count} записей"
    await session.commit()
    await call.message.answer(text)
    
    await dialog_manager.done()


async def on_role_id_input_error(message: Message, dialog_: Any, dialog_manager: DialogManager, error_: ValueError):
    await message.answer("Номер должен быть числом!")


async def on_create_confirmation(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")

    user_id = callback.from_user.id
    name = dialog_manager.find("name").get_value()
    description = dialog_manager.find("description").get_value()
    newRole = RoleDtoBase(
        name=name,
        description=description
    )

    check = await RoleDAO.find_one_or_none(session, newRole)
    if not check:
        await callback.answer("Приступаю к сохранению")
        await RoleDAO.add(session, newRole)
        await callback.answer(f"Должность успешно создано!")
        text = "Должность успешно сохранена"
        await callback.message.answer(text, reply_markup=main_admin_kb())

        await dialog_manager.done()
    else:
        await callback.message.answer("Такая должность уже существует!")
        await dialog_manager.back()

    
async def on_update_confirmation(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")
    
    user_id = callback.from_user.id
    role = await RoleDAO.find_one_or_none_by_id(session ,dialog_manager.dialog_data['role'].id)
    name = dialog_manager.find('name').get_value()
    description = dialog_manager.find('description').get_value()
    
    await callback.answer("Приступаю к сохранению")
        
    role.name = name
    role.description = description

    await session.commit()

    await callback.answer(f"Должность успешно обновлена!")
    text = "Должность успешно сохранена"
    await callback.message.answer(text, reply_markup=main_admin_kb())

    await dialog_manager.done()


async def process_delete_role(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")

    id = dialog_manager.find("id").get_value()
    role = await RoleDAO.find_one_or_none_by_id(session, id)
    
    if role:
        await call.answer("Удаление записи")
        roleDto = RoleDto(
            id=role.id,
            name=role.name,
            description=role.description
        )
        count = await RoleDAO.delete(session, roleDto)
        text = f"Удалено {count} записей"
        await session.commit()
        await call.answer(text)
        
        await dialog_manager.done()
    else:
        await call.answer("Такая должность не существует!\nВведите другой номер.")

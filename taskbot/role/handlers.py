from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from taskbot.dao.dao import RoleDAO
from taskbot.dao.schemas import RoleDtoBase
from taskbot.admin.kbs import main_admin_kb

async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.answer("Сценарий отменен!")
    await callback.message.answer(
        "Вы отменили сценарий.", 
        reply_markup=main_admin_kb(callback.from_user.id)
    )


async def process_add_role(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    session = dialog_manager.middleware_data.get("session_without_commit")
    
    dialog_manager.dialog_data['roles'] = await RoleDAO.find_all(session)
    await dialog_manager.next()


async def on_role_selected(callback: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str):
    session = dialog_manager.middleware_data.get("session_without_commit")
    role_id = int(item_id)
    selected_role = await RoleDAO(session).find_one_or_none_by_id(role_id)

    dialog_manager.dialog_data["selected_role"] = selected_role
    await callback.answer(f"Выбрана должность №{role_id}")
    await dialog_manager.next()

async def on_role_name_input(call: CallbackQuery, windget, dialog_manager: DialogManager):
    name = dialog_manager.find("name").get_vlaue()
    await call.answer(f"Название: {name}")
    await dialog_manager.next()

async def on_role_description_input(call: CallbackQuery, windget, dialog_manager: DialogManager):
    description = dialog_manager.find("description").get_vlaue()
    await call.answer(f"Описание: {description}")
    await dialog_manager.next()


async def on_confirmation(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")

    name = dialog_manager.find("name").get_value()
    description = dialog_manager.find("description").get_value()
    user_id = callback.from_user.id
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
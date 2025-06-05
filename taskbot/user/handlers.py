from typing import Any
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from taskbot.dao.dao import UserDAO, RoleDAO, RegionDAO
from taskbot.dao.schemas import UserDtoBase, UserDtoBase
from taskbot.admin.kbs import main_admin_kb
from taskbot.user.kbs import user_menu_kb
from taskbot.user.state import UserCreate, UserUpdate

async def go_menu(call: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await call.answer("Сценарий отменен!")
    await call.message.answer(
        "Вы отменили сценарий. Меню для должностей:",
        reply_markup=user_menu_kb()
    )

async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.answer("Сценарий отменен!")
    await callback.message.answer(
        "Вы отменили сценарий.", 
        reply_markup=main_admin_kb(callback.from_user.id)
    )


async def on_user_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str):
    session = dialog_manager.middleware_data.get("session_without_commit")
    user_id = int(item_id)
    selected_user = await UserDAO(session).find_one_or_none_by_id(user_id)

    dialog_manager.dialog_data["selected_user"] = selected_user
    await call.answer(f"Выбрана должность №{user_id}")
    await dialog_manager.next()


async def on_user_id_input_error(message: Message, dialog_: Any, dialog_manager: DialogManager, error_: ValueError):
    await message.answer("Номер должен быть числом!")


async def on_create_confirmation(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")

    user_id = callback.from_user.id
    first_name = dialog_manager.find("first_name").get_value()
    last_name = dialog_manager.find("last_name").get_value()
    role_id = dialog_manager.dialog_data["role_id"]
    role = await RoleDAO.find_one_or_none_by_id(session, role_id)
    if role is None:
        await callback.message.answer("Такой должности не существует!")
        return await dialog_manager.switch_to(UserCreate.role)

    if (dialog_manager.dialog_data.get("region_id")):
        region_id = dialog_manager.dialog_data.get("region_id")
        region = await RegionDAO.find_one_or_none_by_id(session, region_id)
        if region is None:
            await callback.message.answer("Такого региона не существует!")
            return await dialog_manager.switch_to(UserCreate.region)

    newuser = UserDtoBase(
        first_name=first_name,
        last_name=last_name,
        role_id=role_id,
        region_id=region_id
    )

    check = await UserDAO.find_one_or_none(session, newuser)
    if not check:
        await callback.answer("Приступаю к сохранению")
        await UserDAO.add(session, newuser)
        await callback.answer(f"Пользователь успешно добавлен!")
        text = "Пользователь успешно добавлен"
        await callback.message.answer(text, reply_markup=main_admin_kb())

        await dialog_manager.done()
    else:
        await callback.message.answer("Этот пользователь уже зарегистрирован!")
        await dialog_manager.back()

    
async def on_update_confirmation(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")
    
    user_id = callback.from_user.id
    id = dialog_manager.find("id").get_value()
    first_name = dialog_manager.find("first_name").get_value()
    last_name = dialog_manager.find("last_name").get_value()
    role_id = dialog_manager.dialog_data["role_id"]
    role = await RoleDAO.find_one_or_none_by_id(session, role_id)
    if role is None:
        await callback.message.answer("Такой должности не существует!")
        return await dialog_manager.switch_to(UserUpdate.role)

    if (dialog_manager.dialog_data.get("region_id")):
        region_id = dialog_manager.dialog_data.get("region_id")
        region = await RegionDAO.find_one_or_none_by_id(session, region_id)
        if region is None:
            await callback.message.answer("Такого региона не существует!")
            return await dialog_manager.switch_to(UserUpdate.region)
    
    check = await UserDAO.find_one_or_none_by_id(session, id)
    if check:
        await callback.answer("Приступаю к сохранению")

        check.first_name = first_name
        check.last_name = last_name
        check.role_id = role_id
        check.region_id = region_id

        await session.commit()

        await callback.answer(f"Запись пользователя успешно обновлена!")
        text = "Запись пользователя успешно сохранена"
        await callback.message.answer(text, reply_markup=main_admin_kb())

        await dialog_manager.done()
    else:
        await callback.message.answer("Запись пользователя не найдена!")
        await dialog_manager.switch_to(UserUpdate.id)


async def process_delete_user(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get("session_with_commit")

    id = dialog_manager.find("id").get_value()
    user = await UserDAO.find_one_or_none_by_id(session, id)
    
    if user:
        await call.answer("Удаление записи")
        userDto = UserDtoBase(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            role_id=user.role_id,
            region_id=user.region_id
        )
        count = await UserDAO.delete(session, userDto)
        text = f"Удалено {count} записей"
        await session.commit()
        await call.answer(text)
        
        await dialog_manager.done()
    else:
        await call.answer("Запись пользователя не найдена!\nВведите другой id.")

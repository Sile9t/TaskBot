from typing import Any
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from ..dao.dao import RegionDAO
from ..dao.schemas import RegionDto, RegionDtoBase
from ..admin.kbs import main_admin_kb
from ..region.kbs import region_menu_kb
from .shemas import FilterRegionById

async def go_menu(call: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    text = "Вы отменили сценарий. Bыход в меню для регионов:"
    await call.message.answer(
        text,
        reply_markup=region_menu_kb()
    )

async def cancel_logic(call: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    userRoleId = auth.role_id if auth else 3
    text = "Сценарий отменен."
    await call.message.answer(
        text, 
        reply_markup=main_admin_kb(userRoleId)
    )


async def on_region_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str, **kwargs):
    session = dialog_manager.middleware_data.get('session_without_commit')
    region_id = int(item_id)
    selected_region = await RegionDAO.find_one_or_none_by_id(session, region_id)
    if (selected_region is None):
        return call.answer(f"Выбраная запись №{region_id} не существует. Выберите еще раз")

    dialog_manager.dialog_data['region_id'] = region_id
    dialog_manager.dialog_data['region'] = selected_region
    await call.answer(f"Выбрана запись №{region_id}")
    await dialog_manager.next()


async def on_region_to_delete_selected(call: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str, **kwargs):
    session = dialog_manager.middleware_data.get("session_without_commit")
    region_id = int(item_id)
    count = await RegionDAO.delete(
        session, 
        FilterRegionById(
            id=region_id
        )
    )

    text = f"Удалено {count} записей"
    await session.commit()
    await call.message.answer(text)

    await dialog_manager.done()

async def on_region_id_input_error(message: Message, dialog_: Any, dialog_manager: DialogManager, error_: ValueError, **kwargs):
    await message.answer("Номер должен быть числом!")

async def add_selected_region_to_dialog(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get('session_without_commit')
    id = dialog_manager.find('id').get_value()
    region = await RegionDAO.find_one_or_none_by_id(session, id)

    dialog_manager.dialog_data['region'] = region


async def on_create_confirmation(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    session = dialog_manager.middleware_data.get("session_with_commit")

    userRoleId = auth.role_id if auth else 3
    user_id = call.from_user.id
    name = dialog_manager.find("name").get_value()
    description = dialog_manager.find("description").get_value()
    newregion = RegionDtoBase(
        name=name,
        description=description
    )

    check = await RegionDAO.find_one_or_none(session, newregion)
    if not check:
        await RegionDAO.add(session, newregion)
        await call.answer(f"Запись успешно создана!")
        text = "Запись успешно сохранена"
        await call.message.answer(text, reply_markup=main_admin_kb(userRoleId))

        await dialog_manager.done()
    else:
        await call.message.answer("Такая запись уже существует!")
        await dialog_manager.back()

    
async def on_update_confirmation(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    auth = dialog_manager.middleware_data.get('auth')
    session = dialog_manager.middleware_data.get('session_with_commit')

    userRoleId = auth.role_id if auth else 3
    region_id = dialog_manager.dialog_data.get('region_id')
    region = await RegionDAO.find_one_or_none_by_id(
        session,
        region_id
    )
    name = dialog_manager.find('name').get_value()
    description = dialog_manager.find('description').get_value()

    if (region):
        region.name = name
        region.description = description

        await session.commit()
        text = "Запись успешно сохранена"
    else: 
        text = "Запись не найдена"

    await call.message.answer(text, reply_markup=main_admin_kb(userRoleId))
    await dialog_manager.done()


async def on_region_wire_confirmation(call: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data.get('session_with_commit')
    id = dialog_manager.find('id').get_value()
    
    region = await RegionDAO.find_one_or_none_by_id(session, id)
    region.chat_id = call.message.chat.id
    regionName = region.name
    
    await session.commit()

    await call.message.delete_reply_markup()
    await call.message.answer(
        text=f"Текущий чат привязан к {regionName}"
    )
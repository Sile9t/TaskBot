from loguru import logger
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from ..admin.kbs import main_admin_kb
from ..dao.models import User

async def cancel_logic(call: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    logger.info(f"chat#{call.message.chat.id}|user#{call.message.from_user.id}: Сценарий отменен.")

    auth = dialog_manager.middleware_data.get('auth')
    userRoleId = auth.role_id if auth else 3

    await call.answer("Сценарий отменен!")
    await call.message.answer(
        "Вы отменили сценарий.", 
        reply_markup=main_admin_kb(userRoleId)
    )

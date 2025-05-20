from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from taskbot.admin.kbs import main_admin_kb, task_kb

async def cancel_logic(call: CallbackQuery, btn: Button, dialog_manager: DialogManager):
    await dialog_manager.done()
    await call.answer("Сценарий отменен!")
    await call.message.answer(
        "Вы отменили сценарий.", 
        reply_markup=main_admin_kb(call.from_user.id)
    )

async def task_menu(call: CallbackQuery, btn: Button, dialog_manager: DialogManager):
    await dialog_manager.done()
    await call.answer("Сценарий отменен!")
    await call.message.answer(
        "Вы отменили сценарий. Выход в меню", 
        reply_markup=task_kb()
    )
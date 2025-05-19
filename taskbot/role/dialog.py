from aiogram_dialog import Dialog
from taskbot.role.windows import get_role_name_window, get_role_description_window, get_confirmation_window

role_dialog = Dialog(
    get_role_name_window(),
    get_role_description_window(),
    get_confirmation_window()
)
from aiogram_dialog import Dialog
from taskbot.task.windows import menu_window, get_id_input_window, get_title_input_window, get_description_input_window

task_dialog = Dialog(
    menu_window(),
    get_id_input_window(),
    get_title_input_window(),
    get_description_input_window()
)
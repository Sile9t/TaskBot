from aiogram_dialog import Dialog
from taskbot.priority.state import PriorityCreate, PriorityUpdate
from taskbot.priority.windows import get_priorities_window, get_priority_id_window, get_priority_value_window, get_priority_title_window, get_priority_description_window, get_create_confirmation_window, get_update_confirmation_window, get_delete_window

priority_create_dialog = Dialog(
    get_priority_value_window(PriorityCreate),
    get_priority_title_window(PriorityCreate),
    get_priority_description_window(PriorityCreate),
    get_create_confirmation_window()
)

priorities_read_dialog = Dialog(
    get_priorities_window()
)

priority_update_dialog = Dialog(
    get_priority_id_window(PriorityUpdate),
    get_priority_value_window(PriorityUpdate),
    get_priority_title_window(PriorityUpdate),
    get_priority_description_window(PriorityUpdate),
    get_update_confirmation_window()
)

priority_delete_dialog = Dialog(
    get_delete_window()
)
from aiogram_dialog import Dialog

from ..status.state import StatusCreate, StatusUpdate
from ..status.windows import get_statuses_window, get_status_id_window, get_status_title_window, get_status_description_window, get_create_confirmation_window, get_update_confirmation_window, get_delete_window

status_create_dialog = Dialog(
    get_status_title_window(StatusCreate),
    get_status_description_window(StatusCreate),
    get_create_confirmation_window()
)

statuses_read_dialog = Dialog(
    get_statuses_window()
)

status_update_dialog = Dialog(
    get_status_id_window(StatusUpdate),
    get_status_title_window(StatusUpdate),
    get_status_description_window(StatusUpdate),
    get_update_confirmation_window()
)

status_delete_dialog = Dialog(
    get_delete_window()
)
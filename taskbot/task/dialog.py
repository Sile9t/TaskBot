from aiogram_dialog import Dialog
from taskbot.task.state import TaskCreate, TaskUpdate
from taskbot.task.windows import get_tasks_window, get_task_id_window, get_task_title_window, get_task_description_window, get_task_startline_window, get_task_deadline_window, get_task_is_active_window, get_task_status_window, get_task_priority_window, get_task_region_window, get_create_confirmation_window, get_update_confirmation_window, get_delete_window


task_create_dialog = Dialog(
    get_task_title_window(TaskCreate),
    get_task_description_window(TaskCreate),
    get_task_startline_window(TaskCreate),
    get_task_deadline_window(TaskCreate),
    get_task_is_active_window(TaskCreate),
    get_task_status_window(TaskCreate),
    get_task_priority_window(TaskCreate),
    get_task_region_window(TaskCreate),
    get_create_confirmation_window()
)

tasks_read_dialog = Dialog(
    get_tasks_window()

)

task_update_dialog = Dialog(
    get_task_id_window(TaskUpdate),
    get_task_title_window(TaskUpdate),
    get_task_description_window(TaskUpdate),
    get_task_startline_window(TaskUpdate),
    get_task_deadline_window(TaskUpdate),
    get_task_is_active_window(TaskUpdate),
    get_task_status_window(TaskUpdate),
    get_task_priority_window(TaskUpdate),
    get_task_region_window(TaskUpdate),
    get_update_confirmation_window()
)

task_delete_dialog = Dialog(
    get_delete_window()
)
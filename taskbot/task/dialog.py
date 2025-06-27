from aiogram_dialog import Dialog

from ..task.state import TaskCreate, TaskUpdate, TaskPriorityUpdate, TaskStatusUpdate, TaskRegionUpdate, TaskPerformersUpdate, TaskDatesUpdate
from ..task.windows import get_tasks_window, get_task_id_window, get_task_title_window, get_task_description_window, get_task_startline_window, get_task_deadline_window, get_task_is_active_window, get_task_status_window, get_task_priority_window, get_task_region_window, get_create_confirmation_window, get_update_confirmation_window, get_delete_window, get_update_task_priority_window, get_update_task_status_window, get_update_task_region_window, get_task_performers_window, get_dates_update_confirmation_window


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

task_priority_change_dialog = Dialog(
    get_task_id_window(TaskPriorityUpdate),
    get_update_task_priority_window(TaskPriorityUpdate)
)

task_status_change_dialog = Dialog(
    get_task_id_window(TaskStatusUpdate),
    get_update_task_status_window(TaskStatusUpdate)
)

task_region_change_dialog = Dialog(
    get_task_id_window(TaskRegionUpdate),
    get_update_task_region_window(TaskRegionUpdate)
)

task_set_performers_dialog = Dialog(
    get_task_id_window(TaskPerformersUpdate),
    get_task_performers_window(TaskPerformersUpdate)
)

task_change_dates_dialog = Dialog(
    get_task_id_window(TaskDatesUpdate),
    get_task_startline_window(TaskDatesUpdate),
    get_task_deadline_window(TaskDatesUpdate),
    get_dates_update_confirmation_window(TaskDatesUpdate)
)
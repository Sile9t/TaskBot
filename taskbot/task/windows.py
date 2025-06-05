import operator
from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, Calendar, CalendarConfig, Back, Cancel, NumberedPager, Row, Next, SwitchTo, CurrentPage, NextPage, PrevPage, FirstPage, LastPage
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.utils import WidgetSrc
from taskbot.task.getters import get_all_tasks, get_confirmed_data, get_is_active_variants
from taskbot.status.windows import get_status_selection_window
from taskbot.status.handlers import on_status_selected
from taskbot.priority.windows import get_priority_selection_window
from taskbot.priority.handlers import on_priority_selected
from taskbot.region.windows import get_region_selection_window
from taskbot.region.handlers import on_region_selected
from taskbot.task.handlers import (
    go_menu, cancel_logic, on_task_selected, on_startline_selected, on_deadline_selected, on_is_active_selected, on_create_confirmation, on_update_confirmation, process_delete_task, on_task_id_input_error,
    on_status_change_selected, on_priority_change_selected, on_region_change_selected
)
from taskbot.task.state import TaskCreate, TaskRead, TaskUpdate, TaskDelete, TaskPriorityUpdate, TaskStatusUpdate, TaskRegionUpdate

MAIN_BTNS = Row(
            Cancel(Const("В меню"), on_click=go_menu),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        )

def get_tasks_window(*widgets: WidgetSrc, state: State = TaskRead.id):
    return Window(
        Format("{text_table}"),
        
        List(
            Format(
                "ID: {item[id]}\n"
                    "Название: {item[title]}\n"
                    "Описание: {item[description]}\n"
                    "Дата начала: {item[startline]}\n"
                    "Дата окончания: {item[deadline]}\n"
                    "Активна: {item[is_active]}\n"
                    "Статус: {item[status]}\n"
                    "Приоритет: {item[priority]}\n"
                    "Регион: {item[region]}\n"
            ),
            items="tasks",
            id='tasks_list',
            page_size=5
        ),

        Row(
            FirstPage(
                scroll="tasks_list", text=Format("⏮️ {target_page1}"),
            ),
            PrevPage(
                scroll="tasks_list", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="tasks_list", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="tasks_list", text=Format("▶️"),
            ),
            LastPage(
                scroll="tasks_list", text=Format("{target_page1} ⏭️"),
            ),
        ),

        *widgets,

        MAIN_BTNS,
        
        getter=get_all_tasks,
        state=state,
    )


def get_task_id_window(stateGroup: StatesGroup = TaskUpdate):
    return get_tasks_window(
        Const("Введите номер задачи для изменения."),
        
        TextInput(
            id="id",
            type_factory=int,
            on_error=on_task_id_input_error,
            on_success=Next()
        ),
        state=stateGroup.id
    )


def get_task_title_window(stateGroup: StatesGroup = TaskCreate):
    return Window(
        Const("Введите название задачи."),
        
        TextInput(
            id="title",
            on_success=Next()
        ),

        MAIN_BTNS,
        
        state=stateGroup.title,
    )


def get_task_description_window(stateGroup: StatesGroup = TaskCreate):
    return Window(
        Const("Введите описание задачи."),
        
        TextInput(
            id="description",
            on_success=Next()
        ),

        Group(
            Next(Const("Пропустить")),         
            MAIN_BTNS,
        ),
        
        state=stateGroup.description,
    )


def get_task_startline_window(stateGroup: StatesGroup = TaskCreate):
    return Window(
        Const("Введите дату начала."),
        
        Calendar(
            id='startline',
            on_click=on_startline_selected
        ),

        MAIN_BTNS,
        
        state=stateGroup.startline,
    )


def get_task_deadline_window(stateGroup: StatesGroup = TaskCreate):
    return Window(
        Const("Введите дату окончания."),
        
        Calendar(
            id='deadline',
            on_click=on_deadline_selected
        ),

        MAIN_BTNS,
        
        state=stateGroup.deadline,
    )


def get_task_is_active_window(stateGroup: StatesGroup = TaskCreate):
    return Window(
        Const("Задача будет обрабатываться ботом?"),
        
        Select(
            Format("{item[0]}"),
            id='is_active',
            item_id_getter=operator.itemgetter(1),
            items='is_active_variants',
            on_click=on_is_active_selected
        ),

        MAIN_BTNS,
        
        state=stateGroup.is_active,
        getter=get_is_active_variants,
    )


def get_task_status_window(stateGroup: StatesGroup = TaskCreate):
    return get_status_selection_window(
        Const("Выберите статус"),
        on_status_click=on_status_selected,
        state=stateGroup.status,
        main_btns=MAIN_BTNS
    )


def get_task_priority_window(stateGroup: StatesGroup = TaskCreate):
    return get_priority_selection_window(
        Const("Выберите приоритет"),
        on_priority_click=on_priority_selected,
        state=stateGroup.priority,
        main_btns=MAIN_BTNS
    )


def get_task_region_window(stateGroup: StatesGroup = TaskCreate):
    return get_region_selection_window(
        Const("Выберите регион"),
        on_region_click=on_region_selected,
        state=stateGroup.region,
        main_btns=MAIN_BTNS
    )


def get_create_confirmation_window():
    return Window(
        Format("{confirmed_text}"),

        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_create_confirmation),
            MAIN_BTNS,
        ),

        state=TaskCreate.confirmation,
        getter=get_confirmed_data
    )


def get_update_confirmation_window():
    return Window(
        Format("{confirmed_text}"),

        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_update_confirmation),
            MAIN_BTNS,
        ),

        state=TaskUpdate.confirmation,
        getter=get_confirmed_data
    )


def get_delete_window():
    return get_tasks_window(
        Const("Введите номер задачи."),
        TextInput(
            id="id",
            type_factory=int,
            on_success=Next(on_click=process_delete_task)
        ),
        state=TaskDelete.id
    )


def get_update_task_status_window(stateGroup: StatesGroup = TaskStatusUpdate):
    return get_status_selection_window(
        Const("Выберите статус"),
        on_status_click=on_status_change_selected,
        state=stateGroup.status,
        main_btns=MAIN_BTNS
    )


def get_update_task_priority_window(stateGroup: StatesGroup = TaskPriorityUpdate):
    return get_priority_selection_window(
        Const("Выберите приоритет"),
        on_priority_click=on_priority_change_selected,
        state=stateGroup.priority,
        main_btns=MAIN_BTNS
    )


def get_update_task_region_window(stateGroup: StatesGroup = TaskRegionUpdate):
    return get_region_selection_window(
        Const("Выберите регион"),
        on_region_click=on_region_change_selected,
        state=stateGroup.region,
        main_btns=MAIN_BTNS
    )
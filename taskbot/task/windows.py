import operator
from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, Calendar, Cancel, Row, Next, CurrentPage, NextPage, PrevPage, FirstPage, LastPage, Multiselect
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.utils import WidgetSrc

from ..task.getters import get_all_tasks, get_confirmed_data, get_is_active_variants, get_changed_dates_data
from ..status.windows import get_status_selection_window
from ..status.handlers import on_status_selected
from ..priority.windows import get_priority_selection_window
from ..priority.handlers import on_priority_selected
from ..region.windows import get_region_selection_window
from ..region.handlers import on_region_to_delete_selected
from ..user.getters import get_performer_id_tuples
from ..task.handlers import (
    go_menu, cancel_logic, on_startline_selected, on_deadline_selected, on_is_active_selected, on_create_confirmation, on_update_confirmation, process_delete_task, on_task_id_input_error,
    on_status_change_selected, on_priority_change_selected, on_region_change_selected, on_performers_selected, on_performer_state_change,
    on_dates_change_confirmation
)
from ..task.state import TaskCreate, TaskRead, TaskUpdate, TaskDelete, TaskPriorityUpdate, TaskStatusUpdate, TaskRegionUpdate, TaskPerformersUpdate, TaskDatesUpdate


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
                    "Исполнители: {item[performers]}\n"
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


def get_task_performers_select_window(*widgets: WidgetSrc, stateGroup: State = TaskPerformersUpdate, main_btns: Row = MAIN_BTNS):
    return Window(
        Format("{text_table}"),

        ScrollingGroup(
            Multiselect(
                Format("✔ {item[0]}"),
                Format(" {item[0]} "),
                id='selected_performers',
                items='performer_id_tuples',
                item_id_getter=operator.itemgetter(1),
                on_state_changed=on_performer_state_change
            ),
            width=1,
            height=5,
            hide_pager=True,
            id='scroll_performers',
        ),

        Row(
            FirstPage(
                scroll="scroll_performers", text=Format("⏮️ {target_page1}"),
            ),
            PrevPage(
                scroll="scroll_performers", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="scroll_performers", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="scroll_performers", text=Format("▶️"),
            ),
            LastPage(
                scroll="scroll_performers", text=Format("{target_page1} ⏭️"),
            ),
        ),

        *widgets,

        Button(Const("Подтвердить"), id="confirm", on_click=on_performers_selected),

        main_btns,
        
        getter=get_performer_id_tuples,
        state=stateGroup.performers,
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
        Const("Выберите дату начала."),
        
        Calendar(
            id='startline',
            on_click=on_startline_selected
        ),

        MAIN_BTNS,
        
        state=stateGroup.startline,
    )


def get_task_deadline_window(stateGroup: StatesGroup = TaskCreate):
    return Window(
        Const("Выберите дату окончания."),
        
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
        on_region_click=on_region_to_delete_selected,
        state=stateGroup.region,
        main_btns=MAIN_BTNS
    )


def get_task_performers_window(stateGroup: StatesGroup = TaskPerformersUpdate):
    return get_task_performers_select_window(
        Const("Выберите исполнителей задания"),
        stateGroup
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


def get_dates_update_confirmation_window(stateGroup: StatesGroup = TaskDatesUpdate):
    return Window(
        Format("{confirmed_text}"),

        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_dates_change_confirmation),
            MAIN_BTNS,
        ),

        state=stateGroup.confirmation,
        getter=get_changed_dates_data
    )

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Back, Next, Cancel, Row, Button, NumberedPager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import List
from taskbot.task.state import TaskForm
from taskbot.task.handlers import cancel_logic, task_menu
from taskbot.task.getters import get_tasks

TASK_MENU_BTN = Row(
            Button(Const("В меню"), id='task_menu', on_click=task_menu),
            Back(Const("Назад")),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        )

def menu_window():
    return Window(
        Format("Menu window"),

        List(
            Format(
                "{item[title]}\n"
            ),
            items='tasks',
            id='task_list',
            page_size=2
        ),

        NumberedPager(
            scroll='task_list',
        ),

        TASK_MENU_BTN,

        getter=get_tasks,
        state=TaskForm.list,
    )

def get_id_input_window():
    return Window(
        Format("Id input window"),

        TextInput(
            id='id',
            type_factory=int,
            on_success=Next(),
        ),

        TASK_MENU_BTN,

        state=TaskForm.id
    )

def get_title_input_window():
    return Window(
        Format("Title input window"),

        TextInput(
            id='title',
            on_success=Next()
        ),

        TASK_MENU_BTN,

        state=TaskForm.title
    )

def get_description_input_window():
    return Window(
        Format("Desc input window"),

        TextInput(
            id=TaskForm.title._state,
            on_success=Next()
        ),

        Next(Const('Пропустить')),
        TASK_MENU_BTN,

        state=TaskForm.description
    )
from operator import itemgetter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, Calendar, CalendarConfig, Back, Cancel, NumberedPager, Row, Next, SwitchTo, CurrentPage, NextPage, PrevPage, FirstPage, LastPage
from aiogram_dialog.widgets.kbd.select import OnItemClick
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.utils import WidgetSrc
from taskbot.priority.getters import get_all_priorities, get_priority_id_tuples, get_confirmed_data
from taskbot.priority.handlers import (
    go_menu, cancel_logic, on_priority_selected, on_create_confirmation, on_update_confirmation, process_delete_priority, on_priority_id_input_error
)
from taskbot.priority.state import PriorityCreate, PriorityRead, PriorityUpdate, PriorityDelete

MAIN_BTNS = Row(
            Cancel(Const("В меню"), on_click=go_menu),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        )

def get_priorities_window(*widgets: WidgetSrc, state: State = PriorityRead.id):
    return Window(
        Format("{text_table}"),
        
        List(
            Format(
                "Приоритет №{item[id]}\n"
                    "Значение: {item[value]}\n"
                    "Название: {item[title]}\n"
                    "Описание: {item[description]}\n"
            ),
            items="priorities",
            id='priorities_list',
            page_size=10
        ),

        Row(
            FirstPage(
                scroll="priorities_list", text=Format("⏮️ {target_page1}"),
            ),
            PrevPage(
                scroll="priorities_list", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="priorities_list", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="priorities_list", text=Format("▶️"),
            ),
            LastPage(
                scroll="priorities_list", text=Format("{target_page1} ⏭️"),
            ),
        ),

        *widgets,

        MAIN_BTNS,
        
        getter=get_all_priorities,
        state=state,
    )


def get_priority_selection_window(*widgets: WidgetSrc, state: State = PriorityUpdate.id, on_priority_click: OnItemClick[Select[str], str] | WidgetEventProcessor | None = on_priority_selected, main_btns: Row = MAIN_BTNS):
    return Window(
        Format("{text_table}"),

        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id='select_priority',
                items='priority_id_tuples',
                item_id_getter=itemgetter(1),
                on_click=on_priority_click
            ),
            width=1,
            height=5,
            hide_pager=True,
            id='scroll_priority',
        ),

        Row(
            FirstPage(
                scroll="scroll_priority", text=Format("⏮️ {target_page1}"),
            ),
            PrevPage(
                scroll="scroll_priority", text=Format("◀️"),
            ),
            CurrentPage(
                scroll="scroll_priority", text=Format("{current_page1}"),
            ),
            NextPage(
                scroll="scroll_priority", text=Format("▶️"),
            ),
            LastPage(
                scroll="scroll_priority", text=Format("{target_page1} ⏭️"),
            ),
        ),

        *widgets,

        main_btns,
        
        getter=get_priority_id_tuples,
        state=state,
    )


def get_priority_id_window(stateGroup: StatesGroup = PriorityUpdate):
    return get_priorities_window(
        Const("Введите номер записи приоритета для изменения."),
        
        TextInput(
            id="id",
            type_factory=int,
            on_error=on_priority_id_input_error,
            on_success=Next()
        ),
        state=stateGroup.id
    )


def get_priority_value_window(stateGroup: StatesGroup = PriorityCreate):
    return Window(
        Const("Введите значение записи приоритета."),
        
        TextInput(
            id="value",
            on_success=Next()
        ),

        MAIN_BTNS,
        
        state=stateGroup.value,
    )


def get_priority_title_window(stateGroup: StatesGroup = PriorityCreate):
    return Window(
        Const("Введите название записи приоритета."),
        
        TextInput(
            id="title",
            on_success=Next()
        ),

        MAIN_BTNS,
        
        state=stateGroup.title,
    )


def get_priority_description_window(stateGroup: StatesGroup = PriorityCreate):
    return Window(
        Const("Введите описание записи приоритета."),
        
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


def get_create_confirmation_window():
    return Window(
        Format("{confirmed_text}"),

        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_create_confirmation),
            MAIN_BTNS,
        ),

        state=PriorityCreate.confirmation,
        getter=get_confirmed_data
    )


def get_update_confirmation_window():
    return Window(
        Format("{confirmed_text}"),

        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_update_confirmation),
            MAIN_BTNS,
        ),

        state=PriorityUpdate.confirmation,
        getter=get_confirmed_data
    )


def get_delete_window():
    return get_priorities_window(
        Const("Введите номер записи приоритета."),
        TextInput(
            id="id",
            type_factory=int,
            on_success=Next(on_click=process_delete_priority)
        ),
        state=PriorityDelete.id
    )

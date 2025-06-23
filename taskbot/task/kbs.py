from typing import List
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def task_menu_kb():
    kb = InlineKeyboardBuilder()
    
    kb.button(text="📋 Список задач", callback_data="task_list")
    kb.button(text="➕ Добавить задачу", callback_data="task_add")
    kb.button(text="🖋 Редактировать задачу", callback_data="task_update")
    kb.button(text="➖ Удалить задачу", callback_data="task_delete")
    kb.button(text="Назад", callback_data="admin_panel")
    kb.adjust(2, 2, 1)

    return kb.as_markup()


def task_update_menu():
    kb = InlineKeyboardBuilder()

    kb.button(text="📋 Изменить полностью", callback_data="task_full_update")
    kb.button(text="✔ Изменить статус", callback_data="task_status_update")
    kb.button(text="🔥 Изменить приоритет", callback_data="task_priority_update")
    kb.button(text="🌍 Изменить регион", callback_data="task_region_update")
    kb.button(text="👷 Назначить исполнителей", callback_data="task_set_performers")
    kb.button(text="В меню", callback_data="admin_panel")
    kb.button(text="Назад", callback_data="task_menu")
    kb.adjust(2, 2, 2)

    return kb.as_markup()

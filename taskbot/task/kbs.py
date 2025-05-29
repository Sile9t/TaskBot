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

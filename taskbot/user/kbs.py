from typing import List
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def menu_kb():
    kb = InlineKeyboardBuilder()
    
    kb.button(text="👩🏻‍💼👨🏻‍💼 Сотрудники", callback_data="employees_list")
    kb.button(text="📋 Задачи", callback_data="tasks_list")
    kb.button(text="📧 Отправить рассылку", callback_data="send_messages")
    kb.adjust(2)

    return kb.as_markup()

def task_kb():
    kb = InlineKeyboardBuilder()

    
    kb.button(text="📋 Список задач", callback_data="task_list")
    kb.button(text="✔ Закрыть задачу", callback_data="task_close")
    kb.button(text="Назад", callback_data="admin_panel")
    kb.adjust(1)
    
    return kb.as_markup()
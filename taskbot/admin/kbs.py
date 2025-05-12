from typing import List
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_kb():
    kb = InlineKeyboardBuilder()
    
    kb.button(text="👩🏻‍💼👨🏻‍💼 Сотрудники", callback_data="employee_menu")
    kb.button(text="📋 Задачи", callback_data="task_menu")
    kb.button(text="✉ Отправить рассылку", callback_data="send_messages")
    kb.adjust(2)

    return kb.as_markup()

def task_kb():
    kb = InlineKeyboardBuilder()

    kb.button(text="📋 Список задач", callback_data="task_list")
    kb.button(text="➕ Добавить задачу", callback_data="task_add")
    kb.button(text="🖋 Редактировать задачу", callback_data="task_edit")
    kb.button(text="➖ Удалить задачу", callback_data="task_delete")
    kb.button(text="✔ Закрыть задачу", callback_data="task_close")
    kb.button(text="Назад", callback_data="admin_panel")
    kb.adjust(1, 2, 2, 1)

    return kb.as_markup()

def employee_kb():
    kb = InlineKeyboardBuilder()
    
    kb.button(text="📋 Список сотрудников", callback_data="employee_list")
    kb.button(text="➕ Добавить сотрудника", callback_data="employee_add")
    kb.button(text="🖋 Редактировать информацию о сотруднике", callback_data="employee_edit")
    kb.button(text="➖ Удалить информацию о сотруднике", callback_data="employee_delete")
    kb.button(text="✔ Изменить роль сотрудника ", callback_data="employee_change_role")
    kb.button(text="Назад", callback_data="admin_panel")
    kb.adjust(1, 2, 2, 1)

    return kb.as_markup()
from typing import List
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def yes_no_kb():
    kb = InlineKeyboardBuilder()

    kb.button(text="Нет", callback_data='no')
    kb.button(text="Да", callback_data='yes')
    kb.adjust(2)

    return kb.as_markup()

def pass_kb():
    kb_list = [
        [KeyboardButton(text='Пропустить')]
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True
    )

def main_admin_kb(user_id: int = -1):
    kb = InlineKeyboardBuilder()
    
    kb.button(text="👩🏻‍💼👨🏻‍💼 Сотрудники", callback_data="user_menu")
    kb.button(text="📋 Задачи", callback_data="task_menu")
    kb.button(text="🎭 Роли", callback_data="role_menu")
    kb.button(text="🌍 Регионы", callback_data="region_menu")
    kb.button(text="✔ Статусы задач", callback_data="status_menu")
    kb.button(text="🔥 Приоритеты задач", callback_data="priority_menu")
    kb.button(text="✉ Отправить рассылку", callback_data="send_messages")
    kb.adjust(2, 2, 2, 1)

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


def task_add_kb():
    return ReplyKeyboardMarkup(
        keyboard=None,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f"title: Название,\ndescription: Описание,\nstartline: Дата начала(дд.мм.гггг),\ndeadline: Дата окончания(дд.мм.гггг),\nis_active: Доступ бота к задаче(True/False),\nstatus_id: Статус задачи,\npriority_id: Приоритет задачи,\nregion_id: Регион"
    )
    

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

def employee_list_kb(page: int = 1, pageCount: int = 1):
    kb = InlineKeyboardBuilder()
    
    if (page > 1):
        kb.button(text="Предыдущие", callback_data=f"role_list_{page+1}")
    if (page < pageCount):
        kb.button(text="Следующие", callback_data=f"role_list_{page-1}")
    kb.button(text="Назад", callback_data="role_menu")
    kb.adjust(2, 1)

    return kb.as_markup()
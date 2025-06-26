from typing import List
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from taskbot.dao.models import User

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

def main_admin_kb(userRoleId: int = 3):
    kb = InlineKeyboardBuilder()
    
    kb.button(text="📋 Задачи", callback_data="task_menu")
    if (userRoleId < 3):
        kb.button(text="👩🏻‍💼👨🏻‍💼 Сотрудники", callback_data="user_menu")
        if (userRoleId < 2):
            kb.button(text="🎭 Должности", callback_data="role_menu")
            kb.button(text="🌍 Регионы", callback_data="region_menu")
            kb.button(text="✔ Статусы задач", callback_data="status_menu")
            kb.button(text="🔥 Приоритеты задач", callback_data="priority_menu")
    kb.adjust(2, 2, 2, 1)

    return kb.as_markup()

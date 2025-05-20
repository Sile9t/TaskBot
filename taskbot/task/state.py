from aiogram.fsm.state import StatesGroup, State

class TaskForm(StatesGroup):
    list = State()
    
    id = State()
    title = State()
    description = State()
    startline = State()
    deadline = State()
    is_active = State()
    status = State()
    priority = State()
    region = State()

    confirmation = State()
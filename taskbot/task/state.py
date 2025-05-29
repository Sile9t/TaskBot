from aiogram.fsm.state import State, StatesGroup

class TaskCreate(StatesGroup):
    title = State()
    description = State()
    startline = State()
    deadline = State()
    is_active = State()
    status = State()
    priority = State()
    region = State()
    confirmation = State()

class TaskRead(StatesGroup):
    id = State() 

class TaskUpdate(StatesGroup):
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

class TaskDelete(StatesGroup):
    id = State()

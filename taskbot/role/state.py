from aiogram.fsm.state import State, StatesGroup

class FormCreate(StatesGroup):
    name = State()
    description = State()
    confirmation = State()

class FormUpdate(StatesGroup):
    name = State()
    description = State()
    check_state = State()

class FormRemove(StatesGroup):
    Id = State()

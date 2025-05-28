from aiogram.fsm.state import State, StatesGroup

class StatusCreate(StatesGroup):
    title = State()
    description = State()
    confirmation = State()

class StatusRead(StatesGroup):
    id = State() 

class StatusUpdate(StatesGroup):
    id = State()
    title = State()
    description = State()
    confirmation = State()

class StatusDelete(StatesGroup):
    id = State()

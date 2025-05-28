from aiogram.fsm.state import State, StatesGroup

class PriorityCreate(StatesGroup):
    value = State()
    title = State()
    description = State()
    confirmation = State()

class PriorityRead(StatesGroup):
    id = State() 

class PriorityUpdate(StatesGroup):
    id = State()
    value = State()
    title = State()
    description = State()
    confirmation = State()

class PriorityDelete(StatesGroup):
    id = State()

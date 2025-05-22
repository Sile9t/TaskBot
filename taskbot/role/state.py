from aiogram.fsm.state import State, StatesGroup

class RoleCreate(StatesGroup):
    name = State()
    description = State()
    confirmation = State()

class RoleRead(StatesGroup):
    id = State() 

class RoleUpdate(StatesGroup):
    id = State()
    name = State()
    description = State()
    confirmation = State()

class RoleDelete(StatesGroup):
    id = State()

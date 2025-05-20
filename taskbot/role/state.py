from aiogram.fsm.state import State, StatesGroup

class RoleForm(StatesGroup):
    id = State()
    name = State()
    description = State()
    confirmation = State()


class FormCreate(StatesGroup):
    name = State()
    description = State()
    confirmation = State()

class FormRead(StatesGroup):
    id = State() 

class FormUpdate(StatesGroup):
    id = State()
    name = State()
    description = State()
    confirmation = State()

class FormRemove(StatesGroup):
    id = State()

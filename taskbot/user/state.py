from aiogram.fsm.state import State, StatesGroup

class UserCreate(StatesGroup):
    first_name = State()
    last_name = State()
    role = State()
    region = State()
    confirmation = State()

class UserRead(StatesGroup):
    id = State() 

class UserUpdate(StatesGroup):
    id = State()
    first_name = State()
    last_name = State()
    role = State()
    region = State()
    confirmation = State()

class UserDelete(StatesGroup):
    id = State()

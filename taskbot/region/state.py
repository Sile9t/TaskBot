from aiogram.fsm.state import State, StatesGroup

class RegionCreate(StatesGroup):
    name = State()
    description = State()
    confirmation = State()

class RegionRead(StatesGroup):
    id = State() 

class RegionUpdate(StatesGroup):
    id = State()
    name = State()
    description = State()
    confirmation = State()

class RegionDelete(StatesGroup):
    id = State()

class RegionWireChat(StatesGroup):
    id = State()
    confirmation = State() 
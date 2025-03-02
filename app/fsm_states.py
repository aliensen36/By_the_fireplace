from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    gender = State()
    profession = State()
    age_group = State()
    place_of_residence = State()
    alone_or_company = State()

# fsm_states.py

from aiogram.fsm.state import State, StatesGroup

class InitialRegistration(StatesGroup):
    choosing_gender = State()
    choosing_profession = State()
    completed_registration = State()

# fsm_states.py

from aiogram.fsm.state import State, StatesGroup

class InitialRegistration(StatesGroup):
    gender = State()
    profession = State()
    completed_registration = State()

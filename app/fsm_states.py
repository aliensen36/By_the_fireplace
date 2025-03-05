from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    gender = State()
    profession = State()
    age_group = State()
    residence = State()

class Survey(StatesGroup):
    company = State()
    reason = State()
    advertising_sources = State()
    visit_frequency = State()
    purpose = State()
    food_preferences = State()
    suggestions = State()
    atmosphere = State()
    service_rating = State()
    improvements = State()
    obstacles = State()

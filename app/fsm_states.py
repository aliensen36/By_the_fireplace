from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    gender = State()
    profession = State()


class SurveyState(StatesGroup):
    age_group = State()
    residence = State()
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
    restaurants = State()
    news = State()
    wishes = State()
    recommendation = State()
    explanation = State()


class FeedbackState(StatesGroup):
    text_to_chat = State()
    text_to_boss = State()


class CallWaiterState(StatesGroup):
    call_waiter = State()


class BookingState(StatesGroup):
    select_date = State()
    select_time = State()
    enter_guests = State()
    confirm = State()
    cancel = State()
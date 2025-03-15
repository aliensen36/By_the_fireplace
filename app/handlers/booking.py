from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app.fsm_states import BookingState
from aiogram.types import CallbackQuery
from datetime import datetime
from utils.calendar import get_calendar
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


booking_router = Router()


def navigation_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅ Назад"), KeyboardButton(text="➡ Далее")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


# Обработчик кнопки '📅🍽️ Забронировать стол'
@booking_router.message(F.text == '📅🍽️ Забронировать стол')
async def start_booking(message: Message, state: FSMContext):
    kb = get_calendar()
    await message.answer('🗓️ Отлично! Давайте забронируем столик.\n\n'
                         '🗓 Выберите дату бронирования:', reply_markup=kb)

    await state.set_state(BookingState.select_date)


# Обработка нажатий по календарю
@booking_router.callback_query(F.data.startswith("select_date:"))
async def process_date(callback: CallbackQuery, state: FSMContext):
    date_str = callback.data.split(":")[1]
    await state.update_data(booking_date=date_str)
    await callback.message.edit_text("Вы выбрали дату:")
    await callback.message.answer(f'✅ <b>{date_str}</b>',
                                  reply_markup=navigation_reply_keyboard(),
                                  parse_mode="HTML")
    await state.set_state(BookingState.select_time)

# Обработка навигации по месяцам
@booking_router.callback_query(F.data.startswith("prev_month:") | F.data.startswith("next_month:"))
async def change_month(callback: CallbackQuery):
    _, month, year = callback.data.split(":")
    month = int(month)
    year = int(year)
    kb = get_calendar(year, month)
    await callback.message.edit_reply_markup(reply_markup=kb)

# Игнорируем ненужные клики
@booking_router.callback_query(F.data == "ignore")
async def ignore(callback: CallbackQuery):
    await callback.answer()

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from app.fsm_states import BookingState
from aiogram.types import CallbackQuery
from datetime import datetime
from utils.calendar import get_calendar
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import app.keyboards.reply as reply_kb
from aiogram.filters import StateFilter


booking_router = Router()


# Доступные временные интервалы для бронирования
TIME_SLOTS = [
    "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
    "18:00", "19:00", "20:00", "21:00"
]


# Функция для создания инлайн-клавиатуры для времени
def time_inline_keyboard():
    keyboard = []
    # Разбиваем список TIME_SLOTS на подсписки по 3 кнопки в каждом
    for i in range(0, len(TIME_SLOTS), 3):
        row = [InlineKeyboardButton(text=slot, callback_data=f"time:{slot}") for slot in TIME_SLOTS[i:i+3]]
        keyboard.append(row)

    # Добавляем кнопку "⬅ Назад" в отдельной строке
    keyboard.append([InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_date")])

    return InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=keyboard
    )


# Функция для создания инлайн-клавиатуры для количества гостей
def guests_inline_keyboard():
    keyboard = []
    for i in range(1, 11, 5):
        row = [
            InlineKeyboardButton(text=str(num), callback_data=f"guests:{num}")
            for num in range(i, i + 5)
        ]
        keyboard.append(row)

    # Добавляем кнопку "⬅ Назад"
    keyboard.append([
        InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_time")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Обработчик кнопки '📅🍽️ Забронировать стол'
@booking_router.message(F.text == '📅🍽️ Забронировать стол')
async def start_booking(message: Message, state: FSMContext):
    await state.set_state(BookingState.select_date)
    kb = get_calendar()
    await message.answer('Отлично! Давайте забронируем столик.\n\n',
                         reply_markup=reply_kb.cancel_keyboard)
    await message.answer('🗓 Выберите дату бронирования:',
                         reply_markup=kb)


# Выбор даты
@booking_router.callback_query(BookingState.select_date,
                               F.data.startswith("select_date:"))
async def select_date(callback: CallbackQuery, state: FSMContext):
    selected_date = callback.data.split(":")[1]
    await state.update_data(select_date=selected_date)
    await callback.message.edit_text(f"Вы выбрали дату: \n\n"
                                     f"✅ <b>{selected_date}</b>",
                                     parse_mode="HTML")
    await callback.message.answer('Теперь выберите время бронирования:',
                                  reply_markup=time_inline_keyboard())
    await state.set_state(BookingState.select_time)


# Обработка навигации по месяцам
@booking_router.callback_query(F.data.startswith("prev_month:") |
                               F.data.startswith("next_month:"))
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


# Выбор времени
@booking_router.message(BookingState.select_time)
async def select_time(message: Message, state: FSMContext):
    await message.answer('Выберите время',
                         reply_markup=time_inline_keyboard())
    await state.set_state(BookingState.select_guests)


# Назад к дате
@booking_router.callback_query(BookingState.select_time,
                               F.data == "back_to_date")
async def back_to_date_from_time(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingState.select_date)
    kb = get_calendar()
    await callback.message.edit_text("Выберите дату:",
                                     reply_markup=kb)


# Выбор времени
@booking_router.callback_query(BookingState.select_time,
                               F.data.startswith("time:"))
async def select_time(callback: CallbackQuery, state: FSMContext):
    select_time = callback.data.split(":")[1]
    if len(select_time) == 2:
        select_time = f"{select_time}:00"
    await state.update_data(select_time=select_time)
    await callback.message.edit_text(f"Вы выбрали время: \n\n"
                                     f"✅ <b>{select_time}</b>",
                                     parse_mode="HTML")
    await callback.message.answer("Теперь выберите количество гостей:",
                                  reply_markup=guests_inline_keyboard())
    await state.set_state(BookingState.select_guests)


# Назад ко времени бронирования
@booking_router.callback_query(BookingState.select_guests,
                               F.data == "back_to_time")
async def back_to_time_from_guests(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingState.select_time)
    await callback.message.edit_text("Выберите время бронирования:",
                                     reply_markup=time_inline_keyboard())



# Выбор количества гостей
@booking_router.callback_query(BookingState.select_guests,
                               F.data.startswith("guests:"))
async def select_guests(callback: CallbackQuery, state: FSMContext):
    select_guests = callback.data.split(":")[1]
    await state.update_data(select_guests=select_guests)
    await callback.message.edit_text(f"Вы указали ✅ <b>{select_guests}</b> "
                                     f"гостей.", parse_mode="HTML")
    await callback.message.answer("Напишите дополнительную информацию "
                                  "по Вашей брони.",
                                  reply_markup=)
    await state.set_state(BookingState.)

kb_skip


# Обработчик
@booking_router.message(F.text == '📅🍽️ Забронировать стол')
async def start_booking(message: Message, state: FSMContext):
    await state.set_state(BookingState.select_date)
    kb = get_calendar()
    await message.answer('Отлично! Давайте забронируем столик.\n\n',
                         reply_markup=reply_kb.cancel_keyboard)
    await message.answer('🗓 Выберите дату бронирования:',
                         reply_markup=kb)

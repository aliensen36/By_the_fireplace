from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from app.fsm_states import BookingState
from aiogram.types import CallbackQuery
from utils.calendar import get_calendar
import app.keyboards.reply as reply_kb
import app.keyboards.inline as inline_kb
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_booking
from datetime import datetime


booking_router = Router()

# Клавиатура с кнопкой "Поделиться номером телефона"
request_phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Поделиться номером телефона", request_contact=True)],
        [KeyboardButton(text="❌ Отменить")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


# Доступные временные интервалы для бронирования
TIME_SLOTS = [
    "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
    "18:00", "19:00", "20:00", "21:00"
]


# Функция для создания инлайн-клавиатуры для времени
def time_inline_keyboard():
    keyboard = []
    for i in range(0, len(TIME_SLOTS), 3):
        row = [InlineKeyboardButton(text=slot, callback_data=f"time:{slot}") for slot in TIME_SLOTS[i:i+3]]
        keyboard.append(row)
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
    keyboard.append([
        InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_time")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


skip = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Пропустить", callback_data="skip")],
    [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_guests")]
])


kb_confirm = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Подтвердить", callback_data="client_confirm")],
    [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_additional_info")]
])


# Обработчик кнопки '📅🍽️ Забронировать стол'
@booking_router.message(F.text == '📅🍽️ Забронировать стол')
async def start_booking(message: Message, state: FSMContext):
    await state.set_state(BookingState.client_name)
    kb = get_calendar()
    await message.answer('Отлично! Давайте забронируем столик.')
    await message.answer('👤 Пожалуйста, введите имя, на кого будет бронирование.',
                         reply_markup=reply_kb.cancel_keyboard)


# Обработка имени клиента
@booking_router.message(BookingState.client_name)
async def get_client_name(message: Message, state: FSMContext):
    client_name = message.text.strip()

    if len(client_name) < 2:
        await message.answer("Имя слишком короткое. Попробуйте еще раз:")
        return

    await state.update_data(client_name=client_name)
    await message.answer(f'Отлично! Столик бронирует <b>{client_name}</b>.',
                         parse_mode="HTML")


    await state.set_state(BookingState.client_phone)
    await message.answer(
        "📞 Пожалуйста, введите номер телефона или нажмите кнопку ниже, "
        "чтобы отправить контакт:",
        reply_markup=request_phone_kb
    )


# Обработка номера телефона
@booking_router.message(BookingState.client_phone)
async def get_client_phone(message: Message, state: FSMContext):
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text.strip()

    if not phone_number.startswith('+') or len(phone_number) < 10:
        await message.answer("Номер телефона выглядит некорректным. Попробуйте снова или нажмите кнопку ниже.",
                            reply_markup=request_phone_kb)
        return

    await state.update_data(client_phone=phone_number)

    await state.set_state(BookingState.select_date)
    kb = get_calendar()
    await message.answer('🗓 Выберите дату бронирования:',
                         reply_markup=kb)


# Выбор даты
@booking_router.callback_query(BookingState.select_date, F.data.startswith("select_date:"))
async def select_date(callback: CallbackQuery, state: FSMContext):
    selected_date_str = callback.data.split(":")[1]
    selected_date = datetime.strptime(selected_date_str, "%d.%m.%Y").date()
    today = datetime.today().date()

    if selected_date < today:
        await callback.answer("Вы не можете выбрать прошедшую дату!", show_alert=True)
        return

    await state.update_data(select_date=selected_date_str)

    await callback.message.edit_text(
        f"Вы выбрали дату: \n\n✅ <b>{selected_date_str}</b>",
        parse_mode="HTML"
    )

    await callback.message.answer(
        "Теперь выберите время бронирования:",
        reply_markup=time_inline_keyboard()
    )

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


# Назад к дате
@booking_router.callback_query(BookingState.select_time,
                               F.data == "back_to_date")
async def back_to_date_from_time(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingState.select_date)
    kb = get_calendar()
    await callback.message.edit_text("Выберите дату:",
                                     reply_markup=kb)


# Выбор количества гостей
@booking_router.callback_query(BookingState.select_guests,
                               F.data.startswith("guests:"))
async def select_guests(callback: CallbackQuery, state: FSMContext):
    select_guests = callback.data.split(":")[1]
    await state.update_data(select_guests=select_guests)
    await callback.message.edit_text(f"Вы указали количество гостей: \n\n"
                                     f" ✅ <b>{select_guests}</b>",
                                     parse_mode="HTML")
    await callback.message.answer("Напишите текстом дополнительную информацию "
                                  "по Вашей брони.",
                                  reply_markup=skip)
    await state.set_state(BookingState.additional_info)


# Назад ко времени бронирования
@booking_router.callback_query(BookingState.select_guests,
                               F.data == "back_to_time")
async def back_to_time_from_guests(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingState.select_time)
    await callback.message.edit_text("Выберите время бронирования:",
                                     reply_markup=time_inline_keyboard())


# Дополнительная информация
@booking_router.message(BookingState.additional_info)
async def additional_info_text(message: Message, state: FSMContext):
    additional_info = message.text
    await state.update_data(additional_info=additional_info)
    data = await state.get_data()
    await message.answer(f"Готово! Данные Вашей брони:\n\n"
                         f"📅 Дата: <b>{data.get('select_date')}</b>\n"
                         f"⏰ Время: <b>{data.get('select_time')}</b>\n"
                         f"👥 Гостей: <b>{data.get('select_guests')}</b>\n"
                         f"📋 Доп. информация: <b>{data.get('additional_info')}</b>",
                         parse_mode="HTML")
    await message.answer("Если всё верно, нажмите 'Подтвердить'!",
                         reply_markup=kb_confirm)
    await state.set_state(BookingState.client_confirm)


# Пропустить дополнительную информацию
@booking_router.callback_query(BookingState.additional_info, F.data == "skip")
async def additional_info_skip(callback: CallbackQuery, state: FSMContext):
    await state.update_data(additional_info="не указана")
    data = await state.get_data()
    await callback.answer()
    await callback.message.edit_text("Готово! Данные Вашей брони:\n\n"
                                     f"📅 Дата: <b>{data.get('select_date')}</b>\n"
                                     f"⏰ Время: <b>{data.get('select_time')}</b>\n"
                                     f"👥 Гостей: <b>{data.get('select_guests')}</b>\n"
                                     f"📋 Доп. информация: <b>{data.get('additional_info')}</b>\n\n"
                                     f"Если всё верно, нажмите 'Подтвердить'!",
                                     parse_mode="HTML",
                                     reply_markup=kb_confirm)
    await state.set_state(BookingState.client_confirm)


# Назад к количеству гостей
@booking_router.callback_query(BookingState.additional_info,
                               F.data == "back_to_guests")
async def back_to_guests_from_additional_info(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingState.select_guests)
    await callback.message.edit_text("Выберите количество гостей:",
                                     reply_markup=guests_inline_keyboard())

# Подтверждение брони
@booking_router.callback_query(BookingState.client_confirm, F.data == "client_confirm")
async def client_confirm(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer()
    await callback.message.answer("🎉 <b>Спасибо за бронирование!</b>\n\n"
                                  "Мы скоро свяжемся с Вами 💬 😊",
                                  parse_mode="HTML",
                                  reply_markup=reply_kb.main)
    data = await state.get_data()
    await orm_booking(session, tg_id=callback.from_user.id, data=data)

    # Отправка брони админам
    bot = callback.bot
    try:
        await bot.send_message(chat_id=-1002551570110,
                               text="Заявка на бронирование стола:\n\n"
                                    f"📅 Дата: <b>{data.get('select_date')}</b>\n"
                                    f"⏰ Время: <b>{data.get('select_time')}</b>\n"
                                    f"👥 Гостей: <b>{data.get('select_guests')}</b>\n"
                                    f"📋 Доп. информация: <b>{data.get('additional_info')}</b>\n\n"
                                    f"👤 Имя: <b>{callback.from_user.first_name}</b>\n"
                                    f"👤 Фамилия: <b>{callback.from_user.last_name}</b>\n"
                                    f"🆔 <b>@{callback.from_user.username}</b>",
                               parse_mode="HTML")
    except Exception as e:
        print(f'Не удалось отправить отзыв директору: {e}')

    await state.clear()



# Назад к дополнительной информации
@booking_router.callback_query(BookingState.client_confirm, F.data == "back_to_additional_info")
async def back_to_additional_info(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_info = data.get("additional_info", "не указана")
    await state.set_state(BookingState.additional_info)
    await callback.message.edit_text(
        f"Дополнительная информация:\n\n<b>{current_info}</b>\n\n"
        "Можете изменить или отправить новую информацию.",
        parse_mode="HTML",
        reply_markup=inline_kb.kb_skip
    )

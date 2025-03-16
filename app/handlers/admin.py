from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from app.filters.chat_types import ChatTypeFilter, IsAdmin
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database.orm_query import get_new_bookings, get_confirmed_bookings
from sqlalchemy import update, select
from datetime import datetime
from database.models import Booking
from aiogram.fsm.context import FSMContext

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


# Главная клавиатура
admin_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Брони')],
],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие')


kb_booking = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Новые заявки')],
    [KeyboardButton(text='Подтвержденные заявки')],
    [KeyboardButton(text='Отмененные заявки')],
    [KeyboardButton(text='⬅️ Назад')],
],
    resize_keyboard=True)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_booking_keyboard(booking_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"admin_confirm:{booking_id}"),
            InlineKeyboardButton(text="❌ Отменить", callback_data=f"admin_cancel:{booking_id}"),
        ],
        [
            InlineKeyboardButton(text="✉️ Написать клиенту", callback_data=f"admin_message:{booking_id}")
        ]
    ])
    return keyboard

# /admin
@admin_router.message(Command("admin"))
async def confirmation(message: Message):
    await message.answer("Что хотите сделать?", reply_markup=admin_main)


@admin_router.message(F.text == 'Брони')
async def booking(message: types.Message):
    await message.answer("Выберите действие", reply_markup=kb_booking)


@admin_router.message(F.text == 'Новые заявки')
async def new_orders(message: types.Message, session: AsyncSession):
    await message.answer("Новые зявки")
    bookings = await get_new_bookings(session)

    if not bookings:
        await message.answer("Нет новых заявок.")
        return

    for b in bookings:
        await message.answer(text='Заявка на бронирование стола\n\n'
                                  f" Номер <b>{b.id}</b>\n"
                                  f" Создана <b>{b.created}</b>\n\n"
                                  f"📅 Дата: <b>{b.select_date.strftime('%d.%m.%Y')}</b>\n"
                                  f"⏰ Время: <b>{b.select_time}</b>\n"
                                  f"👥 Гостей: <b>{b.select_guests}</b>\n"
                                  f"📋 Доп. информация: <b>{b.additional_info}</b>\n\n"
                                  f"👤 Имя: <b>{b.user.first_name}</b>\n"
                                  f"👤 Фамилия: <b>{b.user.last_name}</b>\n"
                                  f"🆔 <b>@{b.user.username}</b>",
                             parse_mode="HTML",
                             reply_markup=admin_booking_keyboard(b.id))


# Подтверждение брони
@admin_router.callback_query(F.data.startswith("admin_confirm"))
async def confirm_booking(callback: CallbackQuery, session: AsyncSession):
    booking_id = int(callback.data.split(":")[1])

    stmt = (
        update(Booking)
        .where(Booking.id == booking_id)
        .values(
            admin_confirm=True,
            admin_action_time=datetime.utcnow(),
            admin_comment="Подтверждено админом"
        )
        .execution_options(synchronize_session="fetch")
    )

    await session.execute(stmt)
    await session.commit()

    # Получаем бронирование, чтобы показать клиенту или админу подтверждение
    booking_stmt = select(Booking).where(Booking.id == booking_id)
    result = await session.execute(booking_stmt)
    booking = result.scalar_one_or_none()

    if booking:
        await callback.message.edit_reply_markup()  # убираем кнопки
        await callback.message.answer(f"✅ Заявка №{booking.id} подтверждена.")

        # Отправка уведомления клиенту:
        await callback.bot.send_message(
            booking.tg_id,
            text=f"✅ Ваша заявка на бронирование подтверждена!\n"
                 f"📅 Дата: {booking.select_date.strftime('%d.%m.%Y')}\n"
                 f"⏰ Время: {booking.select_time}\n"
                 f"👥 Гостей: {booking.select_guests}\n"
                 f"📋 Доп. информация: <b>{booking.additional_info}</b>\n\n"
        )
    else:
        await callback.message.answer("Заявка не найдена.")

    await callback.answer()



@admin_router.message(F.text == 'Подтвержденные заявки')
async def confirmed_orders(message: types.Message, session: AsyncSession):
    await message.answer("Подтвержденные заявки:")
    bookings = await get_confirmed_bookings(session)

    if not bookings:
        await message.answer("Нет подтвержденных заявок.")
        return

    for b in bookings:
        await message.answer(
            text='✅ Подтвержденная заявка на бронирование стола\n\n'
                 f" Номер <b>{b.id}</b>\n"
                 f" Подтверждено <b>{b.admin_action_time.strftime('%d.%m.%Y %H:%M') if b.admin_action_time else '—'}</b>\n\n"
                 f"📅 Дата: <b>{b.select_date.strftime('%d.%m.%Y')}</b>\n"
                 f"⏰ Время: <b>{b.select_time}</b>\n"
                 f"👥 Гостей: <b>{b.select_guests}</b>\n"
                 f"📋 Доп. информация: <b>{b.additional_info}</b>\n\n"
                 f"👤 Имя: <b>{b.user.first_name}</b>\n"
                 f"👤 Фамилия: <b>{b.user.last_name}</b>\n"
                 f"🆔 <b>@{b.user.username}</b>\n"
                 f"💬 Комментарий администратора: <b>{b.admin_comment or '—'}</b>",
            parse_mode="HTML"
        )

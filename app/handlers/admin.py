from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from app.filters.chat_types import ChatTypeFilter, IsAdmin
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from sqlalchemy import select, func
from datetime import datetime, timedelta
from collections import defaultdict

from database.models import User, Booking, Feedback, Survey

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


# Главная клавиатура
admin_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📅 Брони'), KeyboardButton(text='📊 Статистика')],
    [KeyboardButton(text='⬅️ Назад')]
],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие')


@admin_router.message(Command("admin"))
async def confirmation(message: Message):
    await message.answer("Что хотите сделать?", reply_markup=admin_main)


@admin_router.message(F.text == '📊 Статистика')
async def show_statistics(message: Message, session: AsyncSession):
    total_users = await session.scalar(select(func.count()).select_from(User))
    total_bookings = await session.scalar(select(func.count()).select_from(Booking))
    confirmed_bookings = await session.scalar(
        select(func.count()).select_from(Booking).where(Booking.admin_confirm == True)
    )
    cancelled_bookings = await session.scalar(
        select(func.count()).select_from(Booking).where(Booking.admin_cancelled == True)
    )
    total_feedbacks = await session.scalar(select(func.count()).select_from(Feedback))
    total_surveys = await session.scalar(select(func.count()).select_from(Survey))

    # Дополнительно: брони за последнюю неделю
    last_week = datetime.utcnow().date() - timedelta(days=7)
    recent_bookings = await session.scalar(
        select(func.count()).select_from(Booking).where(Booking.select_date >= last_week)
    )

    text = (
        "<b>📊 Статистика чат-бота:</b>\n\n"
        f"👥 Всего пользователей: <b>{total_users}</b>\n"
        f"📅 Всего бронирований: <b>{total_bookings}</b>\n"
        f"✅ Подтверждённых: <b>{confirmed_bookings}</b>\n"
        f"❌ Отклонённых: <b>{cancelled_bookings}</b>\n"
        f"📨 За неделю оформлено: <b>{recent_bookings}</b>\n"
        f"🗣 Отзывов получено: <b>{total_feedbacks}</b>\n"
        f"📝 Заполненных анкет: <b>{total_surveys}</b>"
    )

    await message.answer(text, parse_mode="HTML")


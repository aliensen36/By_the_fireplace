from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from app.filters.chat_types import ChatTypeFilter, IsAdmin
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.fsm_states import BookingState
from database.orm_query import get_new_bookings, get_confirmed_bookings, get_canceled_bookings
from sqlalchemy import update, select
from datetime import datetime
from database.models import Booking
from aiogram.fsm.context import FSMContext
from collections import defaultdict


admin_booking_router = Router()
admin_booking_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


# Главная клавиатура
admin_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📅 Брони'), KeyboardButton(text='📊 Статистика')],
],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие')


kb_booking = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🆕 Новые заявки'), KeyboardButton(text='📊 Сводка броней')],
    [KeyboardButton(text='✅ Подтвержденные заявки'), KeyboardButton(text='❌ Отмененные заявки')],
    [KeyboardButton(text='⬅️  Назад')],
], resize_keyboard=True)


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



@admin_booking_router.message(F.text == '📅 Брони')
async def booking(message: types.Message):
    await message.answer("Выберите действие", reply_markup=kb_booking)


@admin_booking_router.message(F.text == '🆕 Новые заявки')
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
@admin_booking_router.callback_query(F.data.startswith("admin_confirm"))
async def confirm_booking(callback: CallbackQuery, session: AsyncSession):
    booking_id = int(callback.data.split(":")[1])

    stmt = (
        update(Booking)
        .where(Booking.id == booking_id)
        .values(
            admin_confirm=True,
            admin_action_time=datetime.utcnow(),
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
                 f"📋 Доп. информация: <b>{booking.additional_info}</b>",
            parse_mode="HTML",
        )
    else:
        await callback.message.answer("Заявка не найдена.")

    await callback.answer()


# Отмена брони
@admin_booking_router.callback_query(F.data.startswith("admin_cancel"))
async def cancel_booking(callback: CallbackQuery, session: AsyncSession):
    booking_id = int(callback.data.split(":")[1])

    # Запрашиваем комментарий у администратора
    await callback.message.edit_text("❌ Пожалуйста, напишите комментарий для отмены брони.")
    await callback.answer()

    # Ожидаем получения комментария от администратора
    @admin_booking_router.message()
    async def handle_comment(message: types.Message, session: AsyncSession):
        # Получаем комментарий
        admin_comment = message.text

        # Обновляем информацию о бронировании в БД
        stmt = (
            update(Booking)
            .where(Booking.id == booking_id)
            .values(
                admin_cancelled=True,
                admin_action_time=datetime.utcnow(),
                admin_comment=admin_comment,
            )
            .execution_options(synchronize_session="fetch")
        )

        await session.execute(stmt)
        await session.commit()

        # Получаем бронирование, чтобы показать клиенту или админу подтверждение
        booking_stmt = select(Booking).where(Booking.id == booking_id)
        result = await session.execute(booking_stmt)
        booking = result.scalar_one_or_none()
        await message.answer(f"❌ Заявка №{booking.id} отменена.\n\n"
                             f"Комментарий: {admin_comment}")
        if booking:
            await message.answer(f"❌ Заявка №{booking.id} отменена. Комментарий: {admin_comment}")

            # Отправка уведомления клиенту:
            await callback.bot.send_message(
                booking.tg_id,
                text=f"❌ Ваша заявка на бронирование была отменена администратором.\n"
                     f"📅 Дата: {booking.select_date.strftime('%d.%m.%Y')}\n"
                     f"⏰ Время: {booking.select_time}\n"
                     f"👥 Гостей: {booking.select_guests}\n"
                     f"📋 Доп. информация: <b>{booking.additional_info}</b>\n\n"
                     f"💬 Комментарий администратора: <b>{admin_comment}</b>",
                parse_mode="HTML",
            )
        else:
            await message.answer("Заявка не найдена.")


@admin_booking_router.callback_query(F.data.startswith("admin_message"))
async def ask_admin_message(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    booking_id = int(callback.data.split(":")[1])
    await state.update_data(booking_id=booking_id)
    await callback.message.answer("✍️ Введите сообщение, которое хотите отправить клиенту:")
    await state.set_state(BookingState.waiting_for_message)
    await callback.answer()


@admin_booking_router.message(BookingState.waiting_for_message)
async def send_message_to_client(message: types.Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    booking_id = data.get("booking_id")

    # Получаем заявку
    stmt = select(Booking).where(Booking.id == booking_id)
    result = await session.execute(stmt)
    booking = result.scalar_one_or_none()

    if not booking:
        await message.answer("⚠️ Заявка не найдена.")
        await state.clear()
        return

    # Отправляем сообщение клиенту
    try:
        await message.bot.send_message(
            chat_id=booking.tg_id,
            text=f"💬 Сообщение от администратора:\n\n{message.text}"
        )
        await message.answer("✅ Сообщение отправлено клиенту.")
    except Exception as e:
        await message.answer(f"❌ Не удалось отправить сообщение клиенту. Ошибка: {e}")

    await state.clear()


@admin_booking_router.message(F.text == '✅ Подтвержденные заявки')
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


@admin_booking_router.message(F.text == '❌ Отмененные заявки')
async def canceled_orders(message: types.Message, session: AsyncSession):
    await message.answer("Отмененные заявки:")

    # Получаем все отмененные заявки
    bookings = await get_canceled_bookings(session)

    if not bookings:
        await message.answer("Нет отмененных заявок.")
        return

    for b in bookings:
        await message.answer(
            text='❌ Отмененная заявка на бронирование стола\n\n'
                 f" Номер <b>{b.id}</b>\n"
                 f" Отменено <b>{b.admin_action_time.strftime('%d.%m.%Y %H:%M') if b.admin_action_time else '—'}</b>\n\n"
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


@admin_booking_router.message(F.text == '📊 Сводка броней')
async def booking_summary(message: types.Message, session: AsyncSession):
    stmt = (
        select(Booking)
        .where(
            Booking.client_confirm == True,
            Booking.admin_cancelled == False
        )
        .order_by(Booking.select_date, Booking.select_time)
    )
    result = await session.execute(stmt)
    bookings = result.scalars().all()

    if not bookings:
        await message.answer("Список бронирований пуст.")
        return

    summary = defaultdict(list)
    for b in bookings:
        key = f"{b.select_date.strftime('%d.%m.%Y')} — {b.select_time.strftime('%H:%M')}"
        summary[key].append(b)

    text = ("<b>📊 Сводка по бронированиям:</b>\n\n"
            "✓️ - подтвержденные админом\n❓ - неподтвержденные админом\n\n")
    for key, group in summary.items():
        text += f"<b>{key}</b>\n"
        for b in group:
            confirm_status = "✓" if b.admin_confirm else "❓"
            text += (
                f"  • Заявка №{b.id}, гостей: {b.select_guests}, статус: "
                f"{confirm_status}\n"
            )
        text += "\n"

    for part in split_text(text, 4000):
        await message.answer(part, parse_mode="HTML")


def split_text(text, max_length=4000):
    parts = []
    while len(text) > max_length:
        split_index = text.rfind("\n", 0, max_length)
        if split_index == -1:
            split_index = max_length
        parts.append(text[:split_index])
        text = text[split_index:].lstrip()
    parts.append(text)
    return parts


@admin_booking_router.message(F.text == '❌ Отмененные заявки')
async def canceled_orders(message: types.Message, session: AsyncSession):
    await message.answer("Отмененные заявки:")
    stmt = (
        select(Booking)
        .where(Booking.admin_cancelled == True)
        .order_by(Booking.select_date, Booking.select_time)
    )
    result = await session.execute(stmt)
    bookings = result.scalars().all()

    if not bookings:
        await message.answer("Нет отмененных заявок.")
        return

    for b in bookings:
        await message.answer(
            text='❌ Отмененная заявка на бронирование стола\n\n'
                 f" Номер <b>{b.id}</b>\n"
                 f" Отменено <b>{b.admin_action_time.strftime('%d.%m.%Y %H:%M') if b.admin_action_time else '—'}</b>\n\n"
                 f"📅 Дата: <b>{b.select_date.strftime('%d.%m.%Y')}</b>\n"
                 f"⏰ Время: <b>{b.select_time.strftime('%H:%M')}</b>\n"
                 f"👥 Гостей: <b>{b.select_guests}</b>\n"
                 f"📋 Доп. информация: <b>{b.additional_info}</b>\n\n"
                 f"👤 Имя: <b>{b.user.first_name}</b>\n"
                 f"👤 Фамилия: <b>{b.user.last_name}</b>\n"
                 f"🆔 <b>@{b.user.username}</b>\n"
                 f"💬 Комментарий администратора: <b>{b.admin_comment or '—'}</b>",
            parse_mode="HTML"
        )



@admin_booking_router.message(F.text == '⬅️  Назад')
async def go_back_to_admin_menu(message: types.Message):
    await message.answer("Вы вернулись в админ-меню.", reply_markup=admin_main)

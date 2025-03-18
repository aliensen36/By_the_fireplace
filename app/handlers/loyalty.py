import random
from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.filters.chat_types import ChatTypeFilter, IsAdmin
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from sqlalchemy import select, func
from datetime import datetime, timedelta
from collections import defaultdict
from app.fsm_states import BroadcastState, LoyaltyState
from app.text import loyalty_program_message, invite_friend_message
from database.models import *
import app.keyboards.reply as reply_kb
from PIL import Image, ImageDraw, ImageFont


loyalty_router = Router()


async def create_loyalty_card(session: AsyncSession, tg_id: int) -> LoyaltyCard:
    # Создаем карту (без номера)
    new_card = LoyaltyCard(tg_id=tg_id)
    session.add(new_card)
    await session.commit()

    # Получаем id
    await session.refresh(new_card)

    # Генерируем номер карты (например, 100000 + id)
    new_card.card_number = 100000 + new_card.id
    await session.commit()

    return new_card


def generate_loyalty_card(name, surname, card_number, path):
    width, height = 600, 350
    bg_color = "#f2f2f2"
    font_color = "#333333"

    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # Загрузка шрифта
    font = ImageFont.truetype("arial.ttf", 32)
    font_small = ImageFont.truetype("arial.ttf", 24)

    draw.text((40, 60), f"{name} {surname}", font=font, fill=font_color)
    draw.text((40, 120), "Карта лояльности", font=font, fill="#555577")
    draw.text((width - 280, height - 50), f"№ {card_number}", font=font_small, fill="#000000")

    # Сохраняем
    image.save(path)


# Обработчик кнопки '🎁️ Программа лояльности'
@loyalty_router.message(F.text == '🎁️ Программа лояльности')
async def loyalty_program(message: Message):
    await message.answer(loyalty_program_message,
                         reply_markup=reply_kb.kb_loyalty_program)


# Обработчик кнопки '👥 Пригласи друга'
@loyalty_router.message(F.text == '👥 Пригласи друга')
async def invite_friend(message: Message, bot: Bot):
    await message.answer(invite_friend_message)
    url = "https://t.me/myzhenatybot?start=5930bf6439955aa9917a2c30bc9aff2c"
    text = f"Ссылка для приглашения.\n\nСсылку можно передать как в Telegram, " \
             f"так и за его пределы.\n\n{url}"
    button = InlineKeyboardButton(text="Отправить ссылку в ЛС",
                                  switch_inline_query=f"\n\nПриглашаю тебя в бот ресторана "
                                                      f"«У камина»!\n\nПерейди по ссылке:\n\n{url}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer(text, reply_markup=keyboard)


@loyalty_router.message(F.text == "💳 Карта лояльности")
async def loyalty_start(message: Message, state: FSMContext, session: AsyncSession):
    tg_id = message.from_user.id
    result = await session.execute(select(LoyaltyCard).where(LoyaltyCard.tg_id == tg_id))
    card = result.scalar_one_or_none()

    if card:
        # Карта уже есть — показать
        photo_path = f"cards/card_{tg_id}.png"
        try:
            await message.answer_photo(photo=FSInputFile(photo_path),
                                       caption="Ваша карта лояльности 🪪")
        except Exception:
            await message.answer("Карта найдена, но изображение не сгенерировано.")
    else:
        await message.answer("Давайте оформим карту лояльности!\n\nВведите ваше имя:")
        await state.set_state(LoyaltyState.name)


@loyalty_router.message(LoyaltyState.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("Теперь введите вашу фамилию:")
    await state.set_state(LoyaltyState.surname)


@loyalty_router.message(LoyaltyState.surname)
async def get_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text.strip())
    await message.answer("Введите дату рождения (в формате ДД.ММ.ГГГГ):")
    await state.set_state(LoyaltyState.birth_date)


@loyalty_router.message(LoyaltyState.birth_date)
async def get_birth_date(message: Message, state: FSMContext,
                         session: AsyncSession):
    try:
        birth_date = datetime.strptime(message.text.strip(), "%d.%m.%Y").date()
    except ValueError:
        await message.answer("Некорректный формат. "
                             "Пожалуйста, введите дату в формате"
                             " ДД.ММ.ГГГГ.")
        return

    data = await state.get_data()
    name = data['name']
    surname = data['surname']
    tg_id = message.from_user.id

    # Генерация номера карты
    card_number = f"{random.randint(1000,9999)}-{random.randint(1000,9999)}"

    # Используем асинхронный запрос с select
    async with session.begin():
        result = await session.execute(select(User).filter_by(tg_id=tg_id))
        user = result.scalars().first()

        if user:
            user.name = name
            user.surname = surname
            user.birth_date = birth_date

        # Если user не найден, можно создать нового пользователя
        if not user:
            user = User(tg_id=tg_id, name=name, surname=surname, birth_date=birth_date)
            session.add(user)

        # Создание новой карты лояльности
        new_card = LoyaltyCard(
            tg_id=tg_id,
            card_number=card_number,
            user=user
        )
        session.add(new_card)

        # Сохраняем изменения
        await session.commit()

    # Генерация картинки
    photo_path = f"cards/card_{tg_id}.png"
    generate_loyalty_card(name, surname, card_number, photo_path)

    await message.answer_photo(photo=FSInputFile(photo_path),
                               caption="Карта лояльности готова! 🎉")
    await state.clear()

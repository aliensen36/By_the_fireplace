from aiogram.filters import StateFilter
from aiogram.types import (FSInputFile, Message, InlineKeyboardMarkup,
                           InlineKeyboardButton)
from aiogram import F, Router, types, Bot
import app.keyboards.reply as reply_kb
import app.keyboards.inline as inline_kb
from app.fsm_states import FeedbackState
from app.handlers.user_group import user_group_router
from app.handlers.user_group import get_admins
from app.text import *
from database.models import *
from app.fsm_states import *
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert

from database.models import Feedback

router = Router()


# Обработчик кнопки '🍽️ У камина'
@router.message(F.text == '🍽️ У камина')
async def restaurant_description(message: Message):
    link = "https://telegra.ph/MYZHENATY-03-11-2"
    await message.answer(link, parse_mode='Markdown',
                         reply_markup=reply_kb.get_keyboard(
                             '🍽️ У камина', '📋️ Меню', '📅🍽️ Забронировать стол',
                             '🚚️ Доставка', '📍 Путь к нам', '🎁 Программа лояльности',
                             '📝️ Оставить отзыв', '🛎️  Вызов официанта',
                             '📝 Заполнить анкету',
                             placeholder="Что вас интересует?",
                             sizes=(2, 1, 2, 1, 2, 1),
                         )
    )


# Обработчик кнопки '📋️ Меню'
@router.message(F.text == '📋️ Меню')
async def show_menu_options(message: Message):
    await message.answer("Выберите нужное вам меню👇",
                         reply_markup=reply_kb.get_keyboard(
                             '🍽️Основное меню',
                             '👶 Детское меню',
                             '⬅️ Назад',
                             placeholder="Что вас интересует?",
                             sizes=(1,1,1),
                         )
    )


# Обработчик кнопки '🍽️ Основное меню'
@router.message(F.text == '🍽️Основное меню')
async def send_main_menu_pdf(message: Message):
    file_path = 'docs/Main_menu.pdf'
    pdf = FSInputFile(path=file_path, filename='Main_menu.pdf')
    await message.answer_document(document=pdf,
                                  caption="Основное меню центрального зала",
                                  reply_markup=reply_kb.get_keyboard(
                                      '🍽️Основное меню',
                                      '👶 Детское меню',
                                      '⬅️ Назад',
                                      placeholder="Что вас интересует?",
                                      sizes=(1,1,1),
                                  )
                                  )


# Обработчик кнопки '👶 Детское меню'
@router.message(F.text == '👶 Детское меню')
async def show_menu_kids(message: Message):
    link = "https://disk.yandex.ru/i/Qat0Y1HO88Arvw"
    await message.answer(link, parse_mode='Markdown',
                         reply_markup=reply_kb.get_keyboard(
                             '🍽️Основное меню',
                             '👶 Детское меню',
                             '⬅️ Назад',
                             placeholder="Что вас интересует?",
                             sizes=(1,1,1),
                         )
    )


# Обработчик кнопки '⬅️ Назад'
@router.message(F.text == '⬅️ Назад')
async def back_to_main_menu(message: Message):
    await message.answer(text="Выберите 👇",
                         reply_markup=reply_kb.get_keyboard(
                             '🍽️ У камина', '📋️ Меню', '📅🍽️ Забронировать стол',
                             '🚚️ Доставка', '📍 Путь к нам', '🎁 Программа лояльности',
                             '📝️ Оставить отзыв', '🛎️  Вызов официанта', '📝 Заполнить анкету',
                             placeholder="Что вас интересует?",
                             sizes=(2,1,2,1,2,1),
                         )
    )


# Обработчик кнопки '📍 Путь к нам'
@router.message(F.text == '📍 Путь к нам')
async def location(message: Message):
    address = "г. Москва, ул. Лесная, д. 10"
    await message.answer(f"📍 Наш адрес: {address}")
    latitude = 55.778644  # Широта
    longitude = 37.589410  # Долгота
    await message.answer_location(latitude=latitude, longitude=longitude)


# Обработчик кнопки '🚚️ Доставка'
@router.message(F.text == '🚚️ Доставка')
async def delivery(message: Message):
    text = "🍽️ Закажите любое блюдо домой или в офис 🍴\n\nhttps://restoranmyzhenaty.ru/"
    await message.answer(text)


# Обработчик кнопки '🎁️ Программа лояльности'
@router.message(F.text == '🎁 Программа лояльности')
async def loyalty_program(message: Message):
    await message.answer(loyalty_program_message,
                         reply_markup=reply_kb.get_keyboard(
                             '💳 Карта лояльности',
                             '👥 Пригласи друга',
                             '⬅️ Назад',
                             placeholder="Выберите",
                             sizes=(1,1,1))
                         )


# Обработчик кнопки '👥 Пригласи друга'
@router.message(F.text == '👥 Пригласи друга')
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


# Обработчик кнопки '📝️ Оставить отзыв'
@router.message(F.text == '📝️ Оставить отзыв')
async def feedback_menu(message: Message):
    await message.answer('Выбери, пожалуйста, вариант обратной связи👇',
                         reply_markup=reply_kb.get_keyboard(
                             '💬 Оставить отзыв',
                             '✉️ Написать директору',
                             '⬅️ Назад',
                             sizes=(1,1,1),
                         )
    )


# Обработчик кнопки '💬 Оставить отзыв'
@router.message(F.text == '💬 Оставить отзыв')
async def write_feedback(message: Message, state: FSMContext):
    await message.answer('Мы всегда рады любым честным отзывам, так как вы '
                         'помогаете нам повышать уровень сервиса и качество '
                         'обслуживания.\n\nНапишите отзыв и отправьте его в чат 🔽',
                         reply_markup=reply_kb.cancel_keyboard)
    await state.set_state(FeedbackState.text_to_chat)


@router.message(StateFilter(FeedbackState.text_to_chat), Text)
async def receive_feedback_text(message: Message, state: FSMContext,
                                session: AsyncSession):
    await state.update_data(text_to_chat=message.text)

    text_to_chat = message.text
    tg_id = message.from_user.id

    feedback = Feedback(tg_id=tg_id, text_to_chat=text_to_chat)
    session.add(feedback)
    await session.commit()
    await message.answer('Спасибо за ваш отзыв! ❤️')

    # Отправка отзыва в группу админов
    bot = message.bot
    try:
        await bot.send_message(chat_id=-1002551570110,
                               text=f'📬 Новый отзыв от @{message.from_user.username or tg_id}:\n\n{text_to_chat}')
    except Exception as e:
        print(f'Не удалось отправить отзыв в чат: {e}')

    await state.clear()



# Обработчик кнопки '✉️ Написать директору'
@router.message(F.text == '✉️ Написать директору')
async def feedback_to_boss(message: Message):
    await message.answer('📝 Оцените нас от 1 до 10 баллов или напишите '
                         'Свой отзыв и он прямиком улетит владельцу заведения.',
                         reply_markup=reply_kb.cancel_keyboard)


# @router.message(Text)
# async def receive_feedback_text(message: Message, session: AsyncSession):
#     text = message.text
#     tg_id = message.from_user.id
#
#     feedback = Feedback(tg_id=tg_id, text=text)
#     session.add(feedback)
#     await session.commit()
#     await message.answer('Спасибо за ваш отзыв! ❤️')

    # Отправка отзыва админам
    # bot = message.bot
    # user_id = message.from_user.id
    # try:
    #     await message.bot.send_message(user_id=-316851620,
    #                            text=f'📬 Новый отзыв от @{message.from_user.username or tg_id}:\n\n{text}')
    # except Exception as e:
    #     print(f'Не удалось отправить отзыв директору: {e}')


# Обработчик кнопки 'Отмена'
@router.message(F.text == 'Отмена')
async def back_to_main_menu(message: Message):
    await message.answer(text="Выберите 👇",
                         reply_markup=reply_kb.get_keyboard(
                             '💬 Оставить отзыв',
                             '✉️ Написать директору',
                             '⬅️ Назад',
                             sizes=(1,1,1))
                         )

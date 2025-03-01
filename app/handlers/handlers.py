from aiogram.types import (FSInputFile, Message, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram import F, Router, types, Bot
import app.keyboards.reply as reply_kb
import app.keyboards.inline as inline_kb

router = Router()


# Обработчик кнопки '🍽️ У камина'
@router.message(F.text == '🍽️  У камина')
async def restaurant_description(message: Message):
    link = "https://telegra.ph/MYZHENATY-03-11-2"
    await message.answer(link, parse_mode='Markdown',
                         reply_markup=reply_kb.main)


# Обработчик кнопки '📋️ Меню'
@router.message(F.text == '📋️  Меню')
async def show_menu_options(message: Message):
    await message.answer("Выберите нужное вам меню👇",
                         reply_markup=reply_kb.menu_options_keyboard)


# Обработчик кнопки '🍽️ Основное меню'
@router.message(F.text == '🍽️ Основное меню')
async def send_main_menu_pdf(message: Message):
    file_path = 'docs/Main_menu.pdf'
    pdf = FSInputFile(path=file_path, filename='Main_menu.pdf')
    await message.answer_document(document=pdf,
                                  caption="Основное меню центрального зала")


# Обработчик кнопки '👶 Детское меню'
@router.message(F.text == '👶 Детское меню')
async def show_menu_kids(message: Message):
    link = "https://disk.yandex.ru/i/Qat0Y1HO88Arvw"
    await message.answer(link, parse_mode='Markdown',
                         reply_markup=reply_kb.menu_options_keyboard)


# Обработчик кнопки '⬅️ Назад'
@router.message(F.text == '⬅️ Назад')
async def back_to_main_menu(message: Message):
    await message.answer(text="Выберите нужное вам действие👇",
                         reply_markup=reply_kb.main)


# Обработчик кнопки '📍 Путь к нам'
@router.message(F.text == '📍️  Путь к нам')
async def location(message: Message):
    address = "г. Москва, ул. Лесная, д. 10"
    await message.answer(f"📍 Наш адрес: {address}")
    latitude = 55.778644  # Широта
    longitude = 37.589410  # Долгота
    await message.answer_location(latitude=latitude, longitude=longitude)


# Обработчик кнопки '🚚️ Доставка'
@router.message(F.text == '🚚️  Доставка')
async def delivery(message: Message):
    text = "🍽️ Закажите любое блюдо домой или в офис 🍴\n\nhttps://restoranmyzhenaty.ru/"
    await message.answer(text)


# Обработчик кнопки '🎁️ Программа лояльности'
@router.message(F.text == '🎁️  Программа лояльности')
async def loyalty_program(message: Message):
    await message.answer("🥳 10% скидка в День Рождения (действует 1 раз "
                         "в течении 7-ми дней, кроме Реберного зала).\n\n"
                         "☕️ Кофе в подарок при оформлении карты лояльности.\n\n"
                         "🥘 Любое горячее блюдо на выбор за 5-ть приглашенных "
                         "друзей в чат-бот.\n\n⬇️ Выбери нужную кнопку ⬇️",
                         reply_markup=reply_kb.loyalty_program_keyboard)


# Обработчик кнопки '👥 Пригласи друга'
@router.message(F.text == '👥 Пригласи друга')
async def invite_friend(message: Message, bot: Bot):
    text_1 = ("✅ Используйте ссылку ниже, чтобы пригласить друзей в бот.\n\n"
            "Бонус за приглашение друга активируется, когда ваш друг оформит "
            "карту лояльности, находясь в нашем ресторане.\n\n)"
            "Обращаем Ваше внимание, что бонус за приглашение друга не действует, "
            "если ваш друг в момент приглашения уже находится в нашем ресторане.")
    await message.answer(text_1)
    url = "https://t.me/myzhenatybot?start=5930bf6439955aa9917a2c30bc9aff2c"
    text_2 = f"Ссылка для приглашения.\n\nСсылку можно передать как в Telegram, " \
             f"так и за его пределы.\n\n{url}"
    button = InlineKeyboardButton(text="Отправить ссылку в ЛС",
                                  switch_inline_query=f"\n\nПриглашаю тебя в бот ресторана "
                                                      f"«У камина»!\n\nПерейди по ссылке:\n\n{url}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer(text_2, reply_markup=keyboard)



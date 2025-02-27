# handlers.py
import os
from aiogram.filters import CommandStart, Command
from aiogram.methods import SendPhoto
from aiogram.types import (Message, BotCommand, InputFile, BufferedInputFile,
                           FSInputFile, InputFile)
from aiogram import F, Router
import app.keyboards as kb
from aiogram import Bot, Dispatcher, types


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    # Обработка отсутствия username
    if not message.from_user.username:
        photo_ios_path = 'docs/ios_guide.jpg'
        photo_android_path = 'docs/android_guide.jpg'
        ios_instructions = (
            "📱 **IOS**\n\n"
            "1. Нажмите ⚙️Настройки в правом нижнем углу\n"
            "2. Нажмите \"Выбрать имя пользователя\"\n"
            "3. Введите имя пользователя\n"
        )
        android_instructions = (
            "🤖 **Android**\n\n"
            "1. Нажмите на 3 полоски в левом верхнем углу\n"
            "2. Нажмите ⚙️Настройки\n"
            "3. Нажмите на \"Имя пользователя\" и введите имя\n"
        )
        await message.answer_photo(photo=types.FSInputFile(photo_ios_path),
                                 caption=ios_instructions)
        await message.answer_photo(photo=types.FSInputFile(photo_android_path),
                                 caption=android_instructions)
        await message.answer("Для взаимодействия с ботом необходимо задать "
                             "**Username** в настройках Telegram, "
                             "после чего нажмите /start", parse_mode="Markdown")
        return

    await message.answer("Если кнопки скрыты, то нажми на иконку 🎛 в правом "
                         "нижнем углу рядом с микрофоном 👌")
    await message.answer(
        "Привет дорогой друг✋\n"
        "Я виртуальный помощник ресторана \"У камина\"\n\n"
        "Давай познакомимся поближе🤗",
        reply_markup=kb.kb_gender
    )


# Обработчик кнопки '🍽️ У камина'
@router.message(F.text == '🍽️  У камина')
async def restaurant_description(message: Message):
    link = "https://telegra.ph/MYZHENATY-03-11-2"
    await message.answer(link, parse_mode='Markdown', reply_markup=kb.main)


# Обработчик кнопки '📋️ Меню'
@router.message(F.text == '📋️  Меню')
async def show_menu_options(message: Message):
    await message.answer("Выберите нужное вам меню👇",
                         reply_markup=kb.menu_options_keyboard)


# Обработчик кнопки '🍽️ Основное меню'
@router.message(F.text == '🍽️ Основное меню')
async def send_main_menu_pdf(message: types.Message):
    file_path = 'docs/Main_menu.pdf'
    pdf = FSInputFile(path=file_path, filename='Main_menu.pdf')
    await message.answer_document(document=pdf, caption="Основное меню центрального зала")


# Обработчик кнопки '👶 Детское меню'
@router.message(F.text == '👶 Детское меню')
async def show_menu_kids(message: Message):
    link = "https://disk.yandex.ru/i/Qat0Y1HO88Arvw"
    await message.answer(link, parse_mode='Markdown', reply_markup=kb.menu_options_keyboard)


# Обработчик кнопки '⬅️ Назад'
@router.message(F.text == '⬅️ Назад')
async def back_to_main_menu(message: Message):
    await message.answer(text="Выберите нужное вам действие👇", reply_markup=kb.main)

# handlers.py
import os
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand, InputFile, BufferedInputFile, FSInputFile
from aiogram import F, Router
import app.keyboards as kb
from aiogram import Bot, Dispatcher, types


router = Router()

async def set_bot_commands(bot: Bot):
    commands = [BotCommand(command="start", description="Рестарт бота / Обновление меню"),]
    await bot.set_my_commands(commands)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Если кнопки скрыты, то нажми на иконку 🎛 в правом нижнем углу рядом с микрофоном 👌",
                         reply_markup=kb.main)


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

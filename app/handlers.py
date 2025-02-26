# handlers.py

from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from aiogram import F, Router
import app.keyboards as kb
from aiogram import Bot, Dispatcher, types

router = Router()

async def set_bot_commands(bot: Bot):
    commands = [BotCommand(command="start", description="Рестарт бота / Обновление меню"),]
    await bot.set_my_commands(commands)

# @router.message(Command('menu'))
# async def show_menu(message: Message):
#     logo_text = "🍷🔥🍽️ У камина 🍽️🔥🍷"
#     text = (
#         f"{logo_text}\n\n"
#         "Команда <code>/start</code> - Рестарт бота / Обновление меню"
#     )
#     await message.answer(text, parse_mode='HTML', reply_markup=kb.main)

# Обработчик кнопки "🍽️ У камина"
@router.message(F.text == '🍽️  У камина')
async def restaurant_description(message: Message):
    link = "https://telegra.ph/MYZHENATY-03-11-2"
    await message.answer(link, parse_mode='Markdown', reply_markup=kb.main)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Если кнопки скрыты, то нажми на иконку 🎛 в правом нижнем углу рядом с микрофоном 👌",
                         reply_markup=kb.main)



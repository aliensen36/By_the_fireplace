# python run.py

from aiogram import Bot, Dispatcher
import asyncio
from dotenv import load_dotenv
import os
import logging
from app.handlers import router, set_bot_commands

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("https://t.me/Advert202407_bot")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот завершил работу')


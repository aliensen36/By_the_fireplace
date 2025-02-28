# python run.py

from aiogram import Bot, Dispatcher
import asyncio
from dotenv import load_dotenv
import os
import logging
from app.handlers import router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state, State, StatesGroup

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

storage = MemoryStorage()

bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=storage)

user_dict: dict[int, dict[str, str | int | bool]] = {}



async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("https://t.me/Advert202407_bot")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот завершил работу')


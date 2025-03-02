from aiogram.filters import CommandStart, StateFilter
from aiogram.types import (CallbackQuery, Message)
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from sqlalchemy import update, insert, select
from app.fsm_states import InitialRegistration
import app.keyboards.reply as reply_kb
import app.keyboards.inline as inline_kb
from database.engine import session_maker
from database.models import User

start_router = Router()


@start_router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
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

    welcome_message = await message.answer(
        "Привет дорогой друг✋\n"
        "Я виртуальный помощник ресторана \"У камина\"\n\n"
        "Давай познакомимся поближе🤗")

    await state.update_data(welcome_message_id=welcome_message.message_id)
    await state.set_state(InitialRegistration.gender)
    await message.answer("Кто Вы?", reply_markup=inline_kb.kb_gender)


# Обработчик выбора пола
@start_router.callback_query(StateFilter(InitialRegistration.gender), F.data.in_(['male', 'female']))
async def gender_choice(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    welcome_message_id = data.get("welcome_message_id")

    if welcome_message_id:
        try:
            # Удаление приветственного сообщения
            await callback.message.bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=welcome_message_id
            )
        except Exception as e:
            print(f"Ошибка удаления сообщения: {e}")

    await state.update_data(gender=callback.data)
    await state.set_state(InitialRegistration.profession)
    await callback.message.edit_text("Здорово! 😃 \n\nРасскажи, чем ты занимаешься?",
                                     reply_markup=inline_kb.kb_profession)
    await callback.answer()


# Обработчик выбора профессии
@start_router.callback_query(StateFilter(InitialRegistration.profession),
                             F.data.in_(['student', 'businessman',
                                         'employee', 'freelancer']))
async def profession_choice(callback: CallbackQuery, state: FSMContext):
    async with session_maker() as session:
        async with session.begin():
            user_data = await state.get_data()
            user_id = callback.from_user.id
            profession = callback.data
            gender = user_data.get("gender")

            # Проверка наличия пользователя
            result = await session.execute(select(User).where(User.tg_id == user_id))
            user = result.scalars().first()

            if user:
                # Если пользователь уже есть, обновляем
                stmt = (
                    update(User)
                    .where(User.tg_id == user_id)
                    .values(profession=profession, gender=gender)
                )
                await session.execute(stmt)
            else:
                # Если пользователя нет, создаём новую запись
                stmt = insert(User).values(tg_id=user_id, profession=profession, gender=gender)
                await session.execute(stmt)

            await session.commit()

    await state.clear()
    await callback.message.edit_text("Отлично! 👍 \nДля получения скидки 10% остался "
                                     "лишь один шаг.\nПерейди в меню и оформи карту "
                                     "лояльности 💳")
    await callback.message.answer("Если кнопки скрыты, то нажми на иконку 🎛 "
                                  "в правом нижнем углу рядом с микрофоном 👌",
                                  reply_markup=reply_kb.main)
    await callback.answer()
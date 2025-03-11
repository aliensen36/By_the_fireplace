from aiogram.filters import CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from app.fsm_states import Registration
import app.keyboards.reply as reply_kb
import app.keyboards.inline as inline_kb
from app.text import *
from database.orm_query import *

start_router = Router()


@start_router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    is_new_user = await set_user(tg_id)

    if is_new_user:
        await message.answer(welcome_message)
    else:
        await message.answer(
            "Добро пожаловать! 🎉\nС возвращением!",
            reply_markup=reply_kb.main
        )

    # Обработка отсутствия username
    if not message.from_user.username:
        photo_ios_path = 'docs/ios_guide.jpg'
        photo_android_path = 'docs/android_guide.jpg'
        ios_instructions = ios_instructions_message
        android_instructions = android_instructions_message
        await message.answer_photo(photo=types.FSInputFile(photo_ios_path),
                                 caption=ios_instructions)
        await message.answer_photo(photo=types.FSInputFile(photo_android_path),
                                 caption=android_instructions)
        await message.answer("Для взаимодействия с ботом необходимо задать "
                             "**Username** в настройках Telegram, "
                             "после чего нажмите /start", parse_mode="Markdown")
        return

    await state.set_state(Registration.gender)
    await message.answer("Кто Вы?", reply_markup=inline_kb.kb_gender)


@start_router.callback_query(StateFilter(Registration.gender), F.data.in_(['male', 'female']))
async def gender_choice(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)
    await state.set_state(Registration.profession)
    await callback.message.edit_text("Здорово! 😃 \n\nРасскажи, чем ты занимаешься?",
                                     reply_markup=inline_kb.kb_profession)
    await callback.answer()


@start_router.callback_query(StateFilter(Registration.profession),
                             F.data.in_(['student', 'businessman', 'employee', 'freelancer']))
async def profession_choice(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_id = callback.from_user.id
    profession = callback.data
    gender = user_data.get("gender")

    # Обновляем данные пользователя
    await update_user_gender(user_id, gender)
    await update_user_profession(user_id, profession)

    await state.clear()
    await callback.message.edit_text("Отлично! 👍 \nДля получения скидки 10% остался "
                                     "лишь один шаг.\nПерейди в меню и оформи карту "
                                     "лояльности 💳")
    await callback.message.answer("Если кнопки скрыты, то нажми на иконку 🎛 "
                                  "в правом нижнем углу рядом с микрофоном 👌",
                                  reply_markup=reply_kb.main)
    await callback.answer()
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import (CallbackQuery, Message)
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from app.fsm_states import InitialRegistration
import app.keyboards.reply as reply_kb
import app.keyboards.inline as inline_kb
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
    await state.set_state(InitialRegistration.choosing_gender)
    await message.answer("Кто Вы?", reply_markup=inline_kb.kb_gender)



# Обработчик выбора пола
@start_router.callback_query(F.data.in_(['gender_male', 'gender_female']),
                       InitialRegistration.choosing_gender)
async def gender_choice(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    welcome_message_id = data.get("welcome_message_id")

    if welcome_message_id:
        try:
            # Удаляем приветственное сообщение
            await callback.message.bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=welcome_message_id
            )
        except Exception as e:
            print(f"Ошибка удаления сообщения: {e}")

    await state.set_state(InitialRegistration.choosing_profession)  # Переход в следующее состояние
    await callback.message.edit_text("Здорово! 😃 \n\nРасскажи, чем ты занимаешься?",
                                     reply_markup=inline_kb.kb_profession)
    await callback.answer()


# Обработчик выбора профессии
@start_router.callback_query(F.data.in_(['profession_student', 'profession_business',
                                   'profession_employed', 'profession_freelancer']),
                       InitialRegistration.choosing_profession)
async def profession_choice(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(InitialRegistration.completed_registration)
    await callback.message.edit_text("Отлично! 👍 \nДля получения скидки 10% остался "
                                     "лишь один шаг.\nПерейди в меню и оформи карту "
                                     "лояльности 💳")
    await callback.message.answer("Если кнопки скрыты, то нажми на иконку 🎛 "
                                  "в правом нижнем углу рядом с микрофоном 👌",
                                  reply_markup=reply_kb.main)
    await callback.answer()



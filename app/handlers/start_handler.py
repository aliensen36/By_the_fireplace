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
async def cmd_start(message: Message, state: FSMContext,
                    session: AsyncSession):
    # await orm_reg(message=message, session=session)
    # async with session_maker() as session:
    tg_user = message.from_user

    # Обработка отсутствия username
    if not tg_user.username:
        photo_ios_path = 'docs/ios_guide.jpg'
        photo_android_path = 'docs/android_guide.jpg'
        ios_instructions = ios_instructions_message
        android_instructions = android_instructions_message
        await message.answer_photo(photo=FSInputFile(photo_ios_path), caption=ios_instructions)
        await message.answer_photo(photo=FSInputFile(photo_android_path), caption=android_instructions)
        await message.answer(
            "Для взаимодействия с ботом необходимо задать **Username** в настройках Telegram, "
            "после чего нажмите /start", parse_mode="Markdown"
        )
        return

    # Проверка наличия пользователь в БД
    stmt = select(User).where(User.tg_id == tg_user.id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        # Создание пользователя
        user = User(
            tg_id=tg_user.id,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            username=tg_user.username
        )
        session.add(user)
        await session.commit()
        await message.answer(welcome_message)
        await state.set_state(Registration.gender)
        await message.answer("Кто Вы?", reply_markup=inline_kb.kb_gender)
    else:
        # Приветствие зарегистрированного пользователя
        await message.answer(
            "Добро пожаловать! 🎉\nС возвращением!",
            reply_markup=reply_kb.get_keyboard(
                '🍽️ У камина', '📋️ Меню', '📅🍽️ Забронировать стол',
                '🚚️ Доставка', '📍 Путь к нам', '🎁 Программа лояльности',
                '📝️ Оставить отзыв', '🛎️  Вызов официанта', '📝 Заполнить анкету',
                placeholder="Что вас интересует?",
                sizes=(2, 1, 2, 1, 2, 1),
            )
        )


@start_router.callback_query(StateFilter(Registration.gender), F.data.in_(
    ['male', 'female']))
async def gender_choice(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)
    await state.set_state(Registration.profession)
    await callback.message.edit_text("Здорово! 😃 \n\nРасскажи, чем ты занимаешься?",
                                     reply_markup=inline_kb.kb_profession)
    await callback.answer()


@start_router.callback_query(StateFilter(Registration.profession),
                             F.data.in_(['student', 'businessman', 'employee',
                                         'freelancer']))
async def profession_choice(callback: CallbackQuery, state: FSMContext,
                            session: AsyncSession):
    tg_user = callback.from_user
    await state.update_data(profession=callback.data)
    await callback.answer()

    data = await state.get_data()
    gender = data.get('gender')
    profession = data.get('profession')

    stmt = select(User).where(User.tg_id == tg_user.id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        user.gender = gender
        user.profession = profession
        await session.commit()

    await callback.message.edit_text("Отлично! 👍 \nДля получения скидки 10% остался "
                                     "лишь один шаг.\nПерейди в меню и оформи карту "
                                     "лояльности 💳")
    await callback.message.answer("Если кнопки скрыты, то нажми на иконку 🎛 "
                                  "в правом нижнем углу рядом с микрофоном 👌",
                                  reply_markup=reply_kb.get_keyboard(
                                      '🍽️ У камина', '📋️ Меню', '📅🍽️ Забронировать стол',
                                      '🚚️ Доставка', '📍 Путь к нам', '🎁 Программа лояльности',
                                      '📝️ Оставить отзыв', '🛎️  Вызов официанта', '📝 Заполнить анкету',
                                      placeholder="Что вас интересует?",
                                      sizes=(2,1,2,1,2,1)
                                  )
    )
    await state.clear()
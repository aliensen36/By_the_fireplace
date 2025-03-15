from aiogram import F, Router, types
from aiogram.filters import Command

from app.filters.chat_types import ChatTypeFilter, IsAdmin
from app.keyboards.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    'Добавить блюдо',
    'Изменить блюдо',
    'Удалить блюдо',
    'Просмотреть',
    placeholder="Выберите действие",
    sizes=(2,2),
)


@admin_router.message(Command("admin"))
async def add_dish(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == 'Просмотреть')
async def starring_at_dish(message: types.Message):
    await message.answer("Список блюд")


@admin_router.message(F.text == 'Изменить блюдо')
async def change_dish(message: types.Message):
    await message.answer("Список блюд")


@admin_router.message(F.text == "Удалить блюдо")
async def delete_dish(message: types.Message):
    await message.answer("Выберите блюдо для удаления")


@admin_router.message(F.text == "Добавить блюдо")
async def add_dish(message: types.Message):
    await message.answer("Введите название блюда",
                         reply_markup=types.ReplyKeyboardRemove())


@admin_router.message(Command("отмена"))
@admin_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message) -> None:
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@admin_router.message(Command("назад"))
@admin_router.message(F.text.casefold() == "назад")
async def cancel_handler(message: types.Message) -> None:
    await message.answer(f"ок, вы вернулись к прошлому шагу")


@admin_router.message(F.text)
async def add_name(message: types.Message):
    await message.answer("Введите описание блюда")


@admin_router.message(F.text)
async def add_description(message: types.Message):
    await message.answer("Введите стоимость блюда")


@admin_router.message(F.text)
async def add_price(message: types.Message):
    await message.answer("Загрузите изображение блюда")


@admin_router.message(F.photo)
async def add_image(message: types.Message):
    await message.answer("Блюдо добавлено", reply_markup=ADMIN_KB)

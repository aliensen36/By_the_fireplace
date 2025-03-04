from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from database.models import User
from database.engine import session_maker


async def set_user(tg_id: int) -> None:
    """Создание пользователя в БД, если его нет."""
    async with session_maker() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))

            if not user:
                new_user = User(tg_id=tg_id)
                session.add(new_user)
                await session.flush()  # Гарантирует добавление в БД
                await session.commit()

        except SQLAlchemyError as e:
            await session.rollback()  # Откат изменений при ошибке
            print(f"Ошибка при добавлении пользователя: {e}")


async def update_user_gender(tg_id: int, gender: str) -> None:
    """Обновление пола пользователя в БД."""
    async with session_maker() as session:
        try:
            stmt = update(User).where(User.tg_id == tg_id).values(gender=gender)
            await session.execute(stmt)
            await session.commit()

        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Ошибка при обновлении пола: {e}")


async def update_user_profession(tg_id: int, profession: str) -> None:
    """Обновление профессии пользователя в БД."""
    async with session_maker() as session:
        try:
            stmt = update(User).where(User.tg_id == tg_id).values(profession=profession)
            await session.execute(stmt)
            await session.commit()

        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Ошибка при обновлении профессии: {e}")

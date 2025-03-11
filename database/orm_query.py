from sqlalchemy import select, update, insert
from sqlalchemy.exc import SQLAlchemyError
from database.models import User
from database.engine import session_maker


async def set_user(tg_id: int) -> bool:
    """Создание пользователя в БД, если его нет. Возвращает True, если пользователь новый."""
    async with session_maker() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            return True  # Новый пользователь
    return False  # Пользователь уже существовал


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
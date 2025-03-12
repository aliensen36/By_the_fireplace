from sqlalchemy import select, update, insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import *
from database.engine import session_maker


async def orm_set_user(tg_id: int) -> bool:
    """Создание пользователя в БД, если его нет. Возвращает True, если пользователь новый."""
    async with session_maker() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            return True  # Новый пользователь
    return False  # Пользователь уже существовал


async def orm_update_user_gender(tg_id: int, gender: str) -> None:
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


async def orm_survey(session: AsyncSession, user_id: int, data: dict):
    data = Survey(
        user_id=user_id,
        company=data['company'],
        reason=data['reason'],
        advertising_sources=data['advertising_sources'],
        visit_frequency=data['visit_frequency'],
        purpose=data['purpose'],
        food_preferences=data['food_preferences'],
        suggestions=data['suggestions'],
        atmosphere=data['atmosphere'],
        service_rating=data['service_rating'],
        improvements=data['improvements'],
        obstacles=data['obstacles'],
        restaurants=data['restaurants'],
        news=data['news'],
        wishes=data['wishes'],
        recommendation=data['recommendation'],
        explanation=data['explanation'],
    )
    session.add(data)
    await session.commit()
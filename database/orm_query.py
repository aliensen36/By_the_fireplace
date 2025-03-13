from aiogram.types import message, FSInputFile, Message
from sqlalchemy import select, update, insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import *
from database.engine import session_maker



async def orm_survey(session: AsyncSession, tg_id: int, data: dict):
    data = Survey(
        tg_id=tg_id,
        age_group=data['age_group'],
        residence=data['residence'],
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
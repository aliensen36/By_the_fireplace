from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

DATABASE_URL = "postgresql+asyncpg://fireplace_bot_user:fireplace_bot_password@localhost/fireplace_bot_db"

# Создаём движок SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаём сессию для работы с БД
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session_maker() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

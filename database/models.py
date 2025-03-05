from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, DateTime, func, Integer


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    profession: Mapped[str] = mapped_column(String(40), nullable=True)
    age_group: Mapped[str] = mapped_column(String(40), nullable=True)
    residence: Mapped[str] = mapped_column(String, nullable=True)
    company: Mapped[str] = mapped_column(String, nullable=True)
    reason: Mapped[str] = mapped_column(String, nullable=True)
    advertising_sources: Mapped[str] = mapped_column(String, nullable=True)
    visit_frequency: Mapped[str] = mapped_column(String, nullable=True)
    purpose: Mapped[str] = mapped_column(String, nullable=True)
    food_preferences: Mapped[str] = mapped_column(String, nullable=True)
    suggestions: Mapped[str] = mapped_column(String, nullable=True)
    atmosphere: Mapped[str] = mapped_column(String, nullable=True)

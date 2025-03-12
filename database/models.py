from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, DateTime, func, ForeignKey


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    profession: Mapped[str] = mapped_column(String(40), nullable=True)
    age_group: Mapped[str] = mapped_column(String(40), nullable=True)
    residence: Mapped[str] = mapped_column(String(150), nullable=True)

    survey: Mapped[list['Survey']] = relationship(back_populates='user', cascade='all, delete-orphan')


class Survey(Base):
    __tablename__ = 'survey'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    company: Mapped[str] = mapped_column(String(150), nullable=True)
    reason: Mapped[str] = mapped_column(String(150), nullable=True)
    advertising_sources: Mapped[str] = mapped_column(String(150), nullable=True)
    visit_frequency: Mapped[str] = mapped_column(String(150), nullable=True)
    purpose: Mapped[str] = mapped_column(String(150), nullable=True)
    food_preferences: Mapped[str] = mapped_column(String(150), nullable=True)
    suggestions: Mapped[str] = mapped_column(String(150), nullable=True)
    atmosphere: Mapped[str] = mapped_column(String(150), nullable=True)
    service_rating: Mapped[str] = mapped_column(String(150), nullable=True)
    improvements: Mapped[str] = mapped_column(String(150), nullable=True)
    obstacles: Mapped[str] = mapped_column(String(150), nullable=True)
    restaurants: Mapped[str] = mapped_column(String(150), nullable=True)
    news: Mapped[str] = mapped_column(String(150), nullable=True)
    wishes: Mapped[str] = mapped_column(String(300), nullable=True)
    recommendation: Mapped[str] = mapped_column(String(300), nullable=True)

    user: Mapped['User'] = relationship(back_populates='survey')
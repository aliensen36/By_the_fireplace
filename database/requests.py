# from database.models import User
# from sqlalchemy import select
# from database.engine import session_maker
#
#
# async def set_user(tg_id: int) -> None:
#     async with session_maker() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#
#         if not user:
#             session.add(User(tg_id=tg_id))
#             await session.commit()
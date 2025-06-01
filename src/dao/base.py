from sqlalchemy import select

from src.core.bot.bot import db
from src.core.database.core import Database


class BaseDAO:
    model = None

    @classmethod
    async def get_all(cls, **where):
        async for session in db.get_session():
            query = select(cls.model).where(**where)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, model_id: int):
        async for session in db.get_session():
            query = select(cls.model).where(cls.model.id == model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

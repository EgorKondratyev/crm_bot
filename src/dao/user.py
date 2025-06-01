from sqlalchemy import select

from src.core.bot.bot import db
from src.core.database.models import User
from src.core.database.models.user import BusinessRelationshipType
from src.dao.base import BaseDAO


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_by_telegram_id(cls, telegram_id: int) -> model:
        async for session in db.get_session():
            query = select(cls.model).where(cls.model.telegram_id == telegram_id)
            result = await session.execute(query)
            return result.scalars().first()

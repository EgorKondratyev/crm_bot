from src.core.database.models import User
from src.dao.base import BaseDAO


class UserDAO(BaseDAO):
    model = User

from src.core.database.models import Cargo
from src.dao.base import BaseDAO


class CargoDAO(BaseDAO):
    model: Cargo = Cargo

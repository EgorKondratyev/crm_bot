import enum

import sqlalchemy
from sqlalchemy import orm

from src.core.database import mixins
from src.core.database.core import Base


class BusinessRelationshipType(enum.Enum):  # StrEnum python3.11>
    B2B = "B2B"
    B2C = "B2C"
    B2G = "B2G"
    C2C = "C2C"
    B2B2C = "B2B2C"
    G2B = "G2B"
    G2C = "G2C"
    C2B = "C2B"
    P2P = "P2P"


class User(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    telegram_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.BigInteger,
        nullable=False,
    )
    first_name: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(128),
        nullable=True,
    )
    last_name: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(128),
        nullable=True,
    )
    surname: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(128),
        nullable=True,
    )
    email: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(length=255),
        unique=True,
        nullable=True,
    )
    phone_number: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(length=15),
        unique=True,
        nullable=False,
    )
    business_type: orm.Mapped[BusinessRelationshipType] = orm.mapped_column(
        sqlalchemy.Enum(BusinessRelationshipType),
        nullable=False,
    )
    is_blocked: orm.Mapped[bool] = orm.mapped_column(
        sqlalchemy.Boolean,
        default=False,
        nullable=False,
    )

    cargos = orm.relationship(
        "Cargo",
        back_populates="user",
        foreign_keys="[Cargo.user_id]",
        lazy="selectin",
    )

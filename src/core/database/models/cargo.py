import enum

import sqlalchemy
from sqlalchemy import orm

from src.core.database import mixins
from src.core.database.core import Base


class TransportType(enum.Enum):
    TRUCK = "Фура"
    GAZELLE = "Газель"
    MINIVAN = "Микроавтобус"
    CAR = "Легковая машина"


class ShippingType(enum.Enum):
    CARGO = "Грузовая"
    PASSENGER = "Пассажирская"
    EXPRESS = "Срочная"
    COURIER = "Курьерская"
    DANGEROUS = "Опасные грузы"
    REFRIGERATED = "Рефрижераторная"
    INTERNATIONAL = "Международная"
    PACKAGE = "Посылочная"


class CargoStatusType(enum.Enum):
    new = "Новая"
    process = "В обработке"
    finish = "Завершена"


class Cargo(Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    status: orm.Mapped[CargoStatusType] = orm.mapped_column(
        sqlalchemy.Enum(CargoStatusType),
        nullable=False,
        default=CargoStatusType.new,
    )
    height: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.Integer,
        nullable=True,
    )
    width: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.Integer,
        nullable=True,
    )
    weight: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.Integer,
        nullable=False,
    )
    destination_address: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(length=500),
        nullable=False,
    )
    shipping_address: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(length=500),
        nullable=False,
    )
    transport: orm.Mapped[TransportType] = orm.mapped_column(
        sqlalchemy.Enum(TransportType),
        nullable=False,
    )
    shipping: orm.Mapped[ShippingType] = orm.mapped_column(
        sqlalchemy.Enum(ShippingType),
        nullable=True,
    )
    comment_user: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(length=2000),
        nullable=True,
    )
    comment_manager: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(length=2000),
        nullable=True,
    )

    user_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )

    user = orm.relationship(
        "User",
        back_populates="cargos",
        foreign_keys="[Cargo.user_id]",
        lazy="selectin",
    )

"""
init

Revision ID: 7c10342efe35
Revises:   # noqa: UP035
Create Date: 2025-06-01 14:57:35.332526

"""

from typing import Sequence  # noqa: UP035

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7c10342efe35"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("first_name", sa.String(length=128), nullable=True),
        sa.Column("last_name", sa.String(length=128), nullable=True),
        sa.Column("surname", sa.String(length=128), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone_number", sa.String(length=15), nullable=False),
        sa.Column(
            "business_type",
            sa.Enum(
                "B2B",
                "B2C",
                "B2G",
                "C2C",
                "B2B2C",
                "G2B",
                "G2C",
                "C2B",
                "P2P",
                name="businessrelationshiptype",
            ),
            nullable=False,
        ),
        sa.Column("is_blocked", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user")),
        sa.UniqueConstraint("email", name=op.f("uq_user_email")),
        sa.UniqueConstraint("phone_number", name=op.f("uq_user_phone_number")),
    )
    op.create_table(
        "cargo",
        sa.Column(
            "status",
            sa.Enum("new", "process", "finish", name="cargostatustype"),
            nullable=False,
        ),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("weight", sa.Integer(), nullable=False),
        sa.Column("destination_address", sa.String(length=500), nullable=False),
        sa.Column("shipping_address", sa.String(length=500), nullable=False),
        sa.Column(
            "transport",
            sa.Enum("TRUCK", "GAZELLE", "MINIVAN", "CAR", name="transporttype"),
            nullable=False,
        ),
        sa.Column(
            "shipping",
            sa.Enum(
                "CARGO",
                "PASSENGER",
                "EXPRESS",
                "COURIER",
                "DANGEROUS",
                "REFRIGERATED",
                "INTERNATIONAL",
                "PACKAGE",
                name="shippingtype",
            ),
            nullable=True,
        ),
        sa.Column("comment_user", sa.String(length=2000), nullable=True),
        sa.Column("comment_manager", sa.String(length=2000), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("fk_cargo_user_id_user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cargo")),
    )


def downgrade() -> None:
    op.drop_table("cargo")
    op.drop_table("user")

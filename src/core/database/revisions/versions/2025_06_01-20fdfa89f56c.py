"""
telegram id for user

Revision ID: 20fdfa89f56c
Revises: 7c10342efe35  # noqa: UP035
Create Date: 2025-06-01 16:08:39.395516

"""

from typing import Sequence  # noqa: UP035

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20fdfa89f56c"
down_revision: str | None = "7c10342efe35"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("user", sa.Column("telegram_id", sa.BigInteger(), nullable=False))


def downgrade() -> None:
    op.drop_column("user", "telegram_id")

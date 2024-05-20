from datetime import UTC, datetime

import sqlalchemy as sa
from sqlmodel import Field


def created_at_field() -> datetime:
    return Field(default_factory=lambda: datetime.now(UTC))


def updated_at_field() -> datetime:
    return Field(
        sa_column=sa.Column(
            sa.DateTime,
            default=lambda: datetime.now(UTC),
            onupdate=lambda: datetime.now(UTC),
        )
    )

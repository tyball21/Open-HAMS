from datetime import UTC, datetime

import sqlalchemy as sa
from sqlalchemy.types import TIMESTAMP
from sqlmodel import Field


def created_at_field() -> datetime:
    return Field(
        sa_column=sa.Column(
            default=lambda: datetime.now(UTC),
            type_=TIMESTAMP(timezone=True),
        )
    )


def updated_at_field() -> datetime:
    return Field(
        sa_column=sa.Column(
            default=lambda: datetime.now(UTC),
            onupdate=lambda: datetime.now(UTC),
            type_=TIMESTAMP(timezone=True),
        )
    )

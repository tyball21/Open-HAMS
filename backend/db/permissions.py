from typing import Literal, get_args

from sqlalchemy.exc import IntegrityError
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import engine
from models import Permission

PermissionType = Literal[
    "create_events",
    "update_events",
    "delete_events",
    "view_events",
    "add_animal",
    "checkout_animals",
    "checkin_animals",
    "view_animals",
    "update_animals",
    "delete_animals",
    "update_user_tier",
    "update_user_role",
    "update_user_group",
    "add_animal_health_log",
    "create_group",
    "create_event_type",
    "update_event_type",
    "delete_event_type",
    "update_group",
    "create_reports",
    "make_animal_unavailable",
    "make_animal_available",
    "delete_users",
    "create_zoo",
    "update_zoo",
    "delete_zoo",
]

permission_names = get_args(PermissionType)


async def create_permissions() -> None:
    async with AsyncSession(engine) as session:
        for permission_name in permission_names:
            permission = Permission(name=permission_name)
            session.add(permission)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()


async def get_permission(session, name: PermissionType) -> Permission | None:
    permission = (
        await session.exec(select(Permission).where(Permission.name == name))
    ).first()
    return permission


async def get_permissions(
    session, names: list[PermissionType] | None = None
) -> list[Permission]:
    q = select(Permission)
    if names:
        q = q.where(col(Permission.name).in_(names))
    permissions = await session.exec(q)
    return list(permissions.all())


def has_permission(user_permissions: list[Permission], permission: PermissionType):
    return any(p.name == permission for p in user_permissions)

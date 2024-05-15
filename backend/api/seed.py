from core.config import settings
from core.db import engine
from core.security import get_password_hash
from db.users import get_user_by_email
from models import Permission, Role, User
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def seed_roles_and_permissions() -> None:
    async with AsyncSession(engine) as session:
        permissions = [
            Permission(name="manage_animals"),
            Permission(name="manage_events"),
            Permission(name="manage_users"),
            Permission(name="edit_zoo_settings"),
            Permission(name="create_events"),
            Permission(name="checkout_animals"),
            Permission(name="view_animals"),
            Permission(name="view_events"),
            # ... other permissions as necessary ...
        ]

        admin_permissions = permissions
        moderator_permissions = permissions[:2]  # manage_animals, manage_events

        # view_animals, view_events, checkout_animals, create_events
        basic_permissions = permissions[4:]

        roles = [
            Role(name="admin", permissions=admin_permissions),
            Role(name="moderator", permissions=moderator_permissions),
            Role(name="basic", permissions=basic_permissions),
        ]

        for permission in permissions:
            try:
                session.add(permission)
                await session.commit()
                await session.refresh(permission)
            except IntegrityError:
                await session.rollback()

        for role in roles:
            try:
                session.add(role)
                await session.commit()
                await session.refresh(role)
            except Exception:
                await session.rollback()


async def seed_db() -> None:
    await seed_roles_and_permissions()


async def create_admin() -> None:
    async with AsyncSession(engine) as session:
        # check if admin user already exists
        admin_user = await get_user_by_email(settings.ADMIN_EMAIL, session)

        if admin_user:
            return

        user = User(
            email=settings.ADMIN_EMAIL,
            first_name="Admin",
            last_name="User",
            username=settings.ADMIN_USERNAME,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            role=(await session.exec(select(Role).where(Role.name == "admin"))).first(),
        )

        session.add(user)
        await session.commit()

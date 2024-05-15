from core.config import settings
from core.db import engine
from core.security import get_password_hash
from db.roles import get_role
from db.users import get_user_by_email
from db.zoo import get_main_zoo, get_zoo_by_name
from models import Permission, Role, User, Zoo
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession


async def seed_roles_and_permissions() -> None:
    async with AsyncSession(engine) as session:
        permissions = {
            "manage_animals": Permission(name="manage_animals"),
            "manage_events": Permission(name="manage_events"),
            "manage_users": Permission(name="manage_users"),
            "edit_zoo_settings": Permission(name="edit_zoo_settings"),
            "create_events": Permission(name="create_events"),
            "checkout_animals": Permission(name="checkout_animals"),
            "view_animals": Permission(name="view_animals"),
            "view_events": Permission(name="view_events"),
        }

        admin_permissions = [key for key in permissions.keys()]  # all permissions
        moderator_permissions = [
            "view_animals",
            "view_events",
            "manage_animals",
            "manage_events",
        ]

        handler_permissions = [
            "view_animals",
            "view_events",
            "checkout_animals",
            "create_events",
        ]

        visitors_permissions = ["view_animals", "view_events"]

        def get_permissions(permission_list: list[str]):
            return [permissions[permission] for permission in permission_list]

        roles = [
            Role(name="admin", permissions=get_permissions(admin_permissions)),
            Role(name="moderator", permissions=get_permissions(moderator_permissions)),
            Role(name="handler", permissions=get_permissions(handler_permissions)),
            Role(name="visitor", permissions=get_permissions(visitors_permissions)),
        ]

        for permission in permissions.values():
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
            role=await get_role("admin", session),
            zoo=await get_main_zoo(session),
        )

        session.add(user)
        await session.commit()


async def create_zoo() -> None:
    async with AsyncSession(engine) as session:
        zoo_exists = await get_zoo_by_name(settings.ZOO_NAME, session)

        if zoo_exists:
            return

        zoo = Zoo(
            name=settings.ZOO_NAME,
            location=settings.ZOO_LOCATION,
        )

        session.add(zoo)
        await session.commit()

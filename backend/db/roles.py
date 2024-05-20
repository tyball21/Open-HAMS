from sqlmodel import select

from models import Role


async def get_role(name: str, session) -> Role | None:
    role = (await session.exec(select(Role).where(Role.name == name))).first()
    return role

from models import Role
from sqlmodel import Session, select


async def get_role(name: str, session: Session) -> Role | None:
    role = (await session.exec(select(Role).where(Role.name == name))).first()
    return role

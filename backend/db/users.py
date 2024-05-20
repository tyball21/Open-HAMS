from models import User
from sqlmodel import select


async def get_user_by_email(email: str, session) -> User | None:
    user = (await session.exec(select(User).where(User.email == email))).first()
    return user


async def get_user_by_id(id: int, session) -> User | None:
    user = (await session.exec(select(User).where(User.id == id))).first()
    return user


async def get_user_by_username(username: str, session) -> User | None:
    user = (await session.exec(select(User).where(User.username == username))).first()
    return user

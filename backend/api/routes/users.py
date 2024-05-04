from fastapi import APIRouter
from sqlmodel import select

from api.deps import SessionDep
from models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users(session: SessionDep) -> list[User]:
    users = (await session.exec(select(User))).all()
    return users


@router.post("/")
async def create_user(session: SessionDep, user: User) -> User:
    session.add(user)
    await session.commit()
    return user

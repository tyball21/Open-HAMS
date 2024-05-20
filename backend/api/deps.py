from typing import Annotated, AsyncGenerator

from core.db import engine
from core.security import get_token_data
from db.users import get_user_by_username
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from models import User
from schemas import TokenData
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.exceptions import HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = get_token_data(token)
        username: str = payload.get("sub") # type: ignore
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(token_data.username, session) # type: ignore
    if user is None:
        raise credentials_exception
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

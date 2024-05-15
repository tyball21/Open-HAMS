from datetime import timedelta
from typing import Annotated

from api.deps import SessionDep
from core.security import (
    create_access_token,
    get_password_hash,
    get_token_data,
    verify_password,
)
from db.roles import get_role
from db.users import get_user_by_email, get_user_by_id, get_user_by_username
from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from models import Role, User
from schemas import RoleIn, Token, TokenData, UserCreate, UserUpdate
from sqlmodel import select
from starlette.exceptions import HTTPException

router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = get_token_data(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(token_data.username, session)
    print(user.role.name)
    if user is None:
        raise credentials_exception
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    user = await get_user_by_username(form_data.username, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/")
async def get_users(session: SessionDep, _: CurrentUser):
    users = (await session.exec(select(User))).all()
    return users


@router.delete("/")
async def delete_users(session: SessionDep, user: CurrentUser):
    if user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to delete users",
        )

    users = (await session.exec(select(User))).all()
    for user in users:
        await session.delete(user)
    await session.commit()
    return {"message": "All users deleted"}


@router.post("/")
async def create_user(session: SessionDep, user: UserCreate):
    # check if username or email already exists
    user_exists = await get_user_by_username(user.username, session)
    user_exists = user_exists or await get_user_by_email(user.email, session)

    if user_exists:
        raise HTTPException(
            status_code=400, detail="Something went wrong. Please try again."
        )

    # get basic role
    role = (await session.exec(select(Role).where(Role.name == "basic"))).first()

    hashed_password = get_password_hash(user.password)
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        role=role,
    )
    session.add(new_user)
    await session.commit()
    return {"message": "User created"}


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    session: SessionDep,
    current_user: CurrentUser,
    user: UserUpdate = Body(),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized to update this user",
        )

    current_user.first_name = user.first_name
    current_user.last_name = user.last_name
    current_user.username = user.username
    await session.commit()
    return {"message": "Information updated"}


@router.get("/{user_id}")
async def get_user(user_id: int, session: SessionDep, _: CurrentUser):
    user = await get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: SessionDep, current_user: CurrentUser):
    if current_user.role.name != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized to delete this user",
        )

    user = await get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()
    return {"message": "User deleted"}


@router.get("/me")
async def get_authenticated_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/{user_id}/role")
async def update_user_role(
    user_id: int,
    session: SessionDep,
    current_user: CurrentUser,
    role: RoleIn = Body(...),
):
    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to update roles",
        )

    role = await get_role(role.name, session)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    user = await get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role

    await session.commit()
    return {"message": "Role updated"}

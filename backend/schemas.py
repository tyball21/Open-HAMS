from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    username: str = Field(..., min_length=3)


class UserCreate(UserUpdate):
    email: EmailStr
    password: str = Field(..., min_length=8)


class RoleIn(BaseModel):
    name: str

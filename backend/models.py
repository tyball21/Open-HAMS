from datetime import datetime

from core.utils import created_at_field, updated_at_field
from sqlmodel import Field, Relationship, SQLModel


class RolePermission(SQLModel, table=True):
    role_id: int | None = Field(default=None, foreign_key="role.id", primary_key=True)
    permission_id: int | None = Field(
        default=None, foreign_key="permission.id", primary_key=True
    )


class Role(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, unique=True)
    description: str | None = Field(default=None, max_length=1024)

    users: list["User"] = Relationship(back_populates="role")
    permissions: list["Permission"] = Relationship(
        back_populates="roles",
        link_model=RolePermission,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class Permission(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, unique=True)

    roles: list[Role] = Relationship(
        back_populates="permissions",
        link_model=RolePermission,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class Zoo(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=255)
    location: str = Field(max_length=255)
    information: str | None = Field(default=None, max_length=1024)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    animals: list["Animal"] = Relationship(back_populates="zoo")
    users: list["User"] = Relationship(back_populates="zoo")
    event_types: list["EventType"] = Relationship(back_populates="zoo")


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(unique=True)
    first_name: str
    last_name: str
    hashed_password: str
    username: str

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    role_id: int = Field(foreign_key="role.id")
    zoo_id: int | None = Field(foreign_key="zoo.id")

    role: Role = Relationship(back_populates="users", sa_relationship_kwargs={'lazy': 'selectin'})
    zoo: Zoo = Relationship(back_populates="users")
    memberships: list["MemberShip"] = Relationship(back_populates="user")


class Animal(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    kind: str
    species: str
    image: str | None = Field(default=None)
    max_daily_checkouts: int
    max_daily_checkout_hours: int
    rest_time: float

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    zoo_id: int = Field(foreign_key="zoo.id")

    zoo: Zoo = Relationship(back_populates="animals")


class EventType(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    zoo_id: int = Field(foreign_key="zoo.id")

    zoo: Zoo = Relationship(back_populates="event_types")


class MemberShip(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    group_id: int | None = Field(default=None, foreign_key="group.id", primary_key=True)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    group: "Group" = Relationship(back_populates="memberships")
    user: "User" = Relationship(back_populates="memberships")


class Group(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    zoo_id: int = Field(foreign_key="zoo.id")

    memberships: list[MemberShip] = Relationship(back_populates="group")

from datetime import UTC, datetime, timedelta

from core.utils import created_at_field, updated_at_field
from sqlmodel import Field, Relationship, SQLModel


class RolePermission(SQLModel, table=True):
    role_id: int | None = Field(default=None, foreign_key="role.id", primary_key=True)
    permission_id: int | None = Field(
        default=None, foreign_key="permission.id", primary_key=True
    )


class RolePublic(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, unique=True)
    description: str | None = Field(default=None, max_length=1024)


class Role(RolePublic, table=True):
    users: list["User"] = Relationship(back_populates="role")
    permissions: list["Permission"] = Relationship(
        back_populates="roles",
        link_model=RolePermission,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class RoleWithPermissions(RolePublic):
    permissions: list["Permission"] = []


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
    events: list["Event"] = Relationship(back_populates="zoo")
    event_types: list["EventType"] = Relationship(back_populates="zoo")
    groups: list["Group"] = Relationship(back_populates="zoo")


class UserPublic(SQLModel):
    id: int = Field(primary_key=True)
    email: str = Field(unique=True)
    first_name: str
    last_name: str
    username: str
    tier: int = Field(default=1)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    role_id: int = Field(foreign_key="role.id")
    zoo_id: int | None = Field(foreign_key="zoo.id")


class User(UserPublic, table=True):
    hashed_password: str

    role: Role = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy": "selectin"}
    )
    zoo: Zoo = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy": "selectin"}
    )
    memberships: list["MemberShip"] = Relationship(back_populates="user")

    audits: list["AnimalAudit"] = Relationship(back_populates="user")
    comments: list["AnimalComment"] = Relationship(back_populates="user")

    events_link: list["UserEvent"] = Relationship(back_populates="user")


class UserWithRole(UserPublic):
    role: RoleWithPermissions | None = None


class AnimalEvent(SQLModel, table=True):
    __tablename__ = "animal_event"  # type: ignore

    id: int = Field(primary_key=True)

    animal_id: int | None = Field(default=None, foreign_key="animal.id")
    event_id: int | None = Field(default=None, foreign_key="event.id")

    user_in_id: int | None = Field(default=None, foreign_key="user.id")
    user_out_id: int | None = Field(default=None, foreign_key="user.id")

    checked_in: datetime | None = Field(default=None)
    checked_out: datetime | None = Field(default=None)

    duration: timedelta | None = Field(default=None)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    animal: "Animal" = Relationship(back_populates="events_link")
    event: "Event" = Relationship(back_populates="animals_link")


class AnimalIn(SQLModel):
    name: str
    kind: str
    species: str
    image: str | None = Field(default=None)
    max_daily_checkouts: int
    max_daily_checkout_hours: int
    rest_time: float
    description: str | None = Field(default=None)
    tier: int = Field(default=1)

    daily_checkout_count: int = Field(default=0)
    daily_checkout_duration: timedelta = Field(default=timedelta(hours=0))
    last_checkin_time: datetime | None = Field(default=None)
    checked_in: bool = Field(default=True)
    handling_enabled: bool

    zoo_id: int = Field(foreign_key="zoo.id")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Lion",
                    "kind": "Mammal",
                    "species": "Panthera leo",
                    "image": "https://example.com/lion.jpg",
                    "max_daily_checkouts": 10,
                    "max_daily_checkout_hours": 2,
                    "rest_time": 1.5,
                    "description": "The lion is a species in the family Felidae and a member of the genus Panthera.",
                    "handling_enabled": True,
                    "zoo_id": 1,
                    "tier": 1,
                }
            ]
        }
    }  # type: ignore


class Animal(AnimalIn, table=True):
    id: int = Field(primary_key=True)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    zoo: Zoo = Relationship(back_populates="animals")
    events_link: list[AnimalEvent] = Relationship(back_populates="animal")
    activity_logs: list["AnimalActitvityLog"] = Relationship(back_populates="animal")
    audits: list["AnimalAudit"] = Relationship(back_populates="animal")
    health_logs: list["AnimalHealthLog"] = Relationship(back_populates="animal")
    comments: list["AnimalComment"] = Relationship(back_populates="animal")


class EventTypeIn(SQLModel):
    name: str
    zoo_id: int = Field(foreign_key="zoo.id")


class EventType(EventTypeIn, table=True):
    __tablename__ = "event_type"  # type: ignore

    id: int = Field(primary_key=True)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    zoo: Zoo = Relationship(back_populates="event_types")

    events: list["Event"] = Relationship(back_populates="event_type")


class EventIn(SQLModel):
    event_type_id: int
    name: str
    description: str
    start_at: datetime
    end_at: datetime
    event_type_id: int = Field(foreign_key="event_type.id")
    zoo_id: int = Field(foreign_key="zoo.id")


class Event(EventIn, table=True):
    id: int = Field(primary_key=True)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    event_type: EventType = Relationship(
        back_populates="events", sa_relationship_kwargs={"lazy": "selectin"}
    )

    zoo: Zoo = Relationship(back_populates="events")
    animals_link: list[AnimalEvent] = Relationship(back_populates="event")
    comments: list["AnimalComment"] = Relationship(back_populates="event")

    users_link: list["UserEvent"] = Relationship(back_populates="event")


class MemberShip(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    group_id: int | None = Field(default=None, foreign_key="group.id", primary_key=True)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    group: "Group" = Relationship(back_populates="memberships")
    user: "User" = Relationship(back_populates="memberships")


class GroupIn(SQLModel):
    title: str
    zoo_id: int = Field(foreign_key="zoo.id")


class GroupPublic(GroupIn):
    id: int = Field(primary_key=True)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()


class Group(GroupPublic, table=True):
    zoo: Zoo = Relationship(
        back_populates="groups", sa_relationship_kwargs={"lazy": "selectin"}
    )
    memberships: list[MemberShip] = Relationship(back_populates="group")


class GroupWithZoo(GroupPublic):
    zoo: Zoo | None = None


class AnimalActitvityLog(SQLModel, table=True):
    __tablename__ = "animal_activity_log"  # type: ignore

    id: int = Field(primary_key=True)
    animal_id: int = Field(foreign_key="animal.id")
    details: str
    logged_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    animal: Animal = Relationship(back_populates="activity_logs")


class AnimalAudit(SQLModel, table=True):
    __tablename__ = "animal_audit"  # type: ignore

    id: int = Field(primary_key=True)
    animal_id: int = Field(foreign_key="animal.id")
    changed_field: str
    old_value: str | None = Field(default=None)
    new_value: str | None = Field(default=None)

    changed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    changed_by: int = Field(foreign_key="user.id")

    user: User = Relationship(back_populates="audits")
    animal: Animal = Relationship(back_populates="audits")


class AnimalHealthLog(SQLModel, table=True):
    __tablename__ = "animal_health_log"  # type: ignore

    id: int = Field(primary_key=True)
    animal_id: int = Field(foreign_key="animal.id")
    details: str
    logged_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    animal: Animal = Relationship(back_populates="health_logs")


class AnimalCommentIn(SQLModel):
    comment: str


class AnimalComment(AnimalCommentIn, table=True):
    __table_name__ = "animal_comment"  # type: ignore

    id: int = Field(primary_key=True)
    animal_id: int = Field(foreign_key="animal.id")
    user_id: int = Field(foreign_key="user.id")
    event_id: int | None = Field(foreign_key="event.id", default=None)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    animal: Animal = Relationship(back_populates="comments")
    user: User = Relationship(back_populates="comments")
    event: Event = Relationship(back_populates="comments")


class UserEvent(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    event_id: int | None = Field(default=None, foreign_key="event.id", primary_key=True)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    user: User = Relationship(back_populates="events_link")
    event: Event = Relationship(back_populates="users_link")


# Composite models
class EventWithAnimals(SQLModel):
    event: Event
    animals: list[Animal]


class GroupWithMembers(SQLModel):
    group: GroupWithZoo
    members: list[UserPublic]

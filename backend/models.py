from datetime import UTC, datetime, timedelta
from typing import Literal

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy import Index
from sqlalchemy.types import TIMESTAMP
from sqlmodel import Field, Relationship, SQLModel

from core.utils import created_at_field, updated_at_field


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
        sa_relationship_kwargs={"lazy": "joined"},
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


class PasswordResetToken(SQLModel, table=True):
    __tablename__ = "password_reset_token"  # type: ignore

    id: int = Field(primary_key=True)
    token: str
    user_id: int = Field(foreign_key="user.id")
    expires_at: datetime = Field(
        sa_column=sa.Column(
            type_=TIMESTAMP(timezone=True),
        )
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
    users: list["User"] = Relationship(back_populates="group")
    event_types: list["EventType"] = Relationship(back_populates="group")

    __table_args__ = (Index("ix_unique_title_zoo_id", "title", "zoo_id", unique=True),)


class GroupWithZoo(GroupPublic):
    zoo: Zoo | None = None


class UserPublic(SQLModel):
    id: int = Field(primary_key=True)
    email: str = Field(unique=True)
    first_name: str
    last_name: str
    username: str
    tier: int = Field(default=1)
    image: str | None = Field(default=None)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    role_id: int = Field(foreign_key="role.id")
    zoo_id: int | None = Field(foreign_key="zoo.id")
    group_id: int | None = Field(foreign_key="group.id", default=None)


class User(UserPublic, table=True):
    hashed_password: str

    role: Role = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy": "joined"}
    )
    zoo: Zoo = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy": "joined"}
    )
    group: "Group" = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy": "joined"}
    )

    audits: list["AnimalAudit"] = Relationship(back_populates="user")
    comments: list["EventComment"] = Relationship(back_populates="user")
    health_logs: list["AnimalHealthLog"] = Relationship(back_populates="user")
    events_link: list["UserEvent"] = Relationship(back_populates="user")


class UserWithDetails(UserPublic):
    role: RoleWithPermissions | None = None
    group: Group | None = None  # type: ignore
    zoo: Zoo | None = None


class AnimalEvent(SQLModel, table=True):
    __tablename__ = "animal_event"  # type: ignore

    id: int = Field(primary_key=True)

    animal_id: int = Field(default=None, foreign_key="animal.id")
    event_id: int = Field(default=None, foreign_key="event.id")

    user_in_id: int | None = Field(default=None, foreign_key="user.id")
    user_out_id: int | None = Field(default=None, foreign_key="user.id")

    checked_in: datetime | None = Field(
        default=None,
        sa_column=sa.Column(
            type_=TIMESTAMP(timezone=True),
        ),
    )
    checked_out: datetime | None = Field(
        default=None,
        sa_column=sa.Column(
            type_=TIMESTAMP(timezone=True),
        ),
    )

    duration: timedelta | None = Field(default=None)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    animal: "Animal" = Relationship(back_populates="events_link")
    event: "Event" = Relationship(back_populates="animals_link")


class AnimalIn(SQLModel):
    name: str
    species: str
    image_filename: str | None = Field(default=None)
    max_daily_checkouts: int
    max_daily_checkout_hours: int | None = Field(default=None)
    rest_time: float | None = Field(default=None)
    description: str | None = Field(default=None)
    tier: int = Field(default=1)

    daily_checkout_count: int = Field(default=0)
    daily_checkout_duration: timedelta = Field(default=timedelta(hours=0))
    last_checkin_time: datetime | None = Field(
        default=None,
        sa_column=sa.Column(
            type_=TIMESTAMP(timezone=True),
        ),
    )
    checked_in: bool = Field(default=True)
    handling_enabled: bool
    status: str | None = Field(default="checked_in")

    zoo_id: int = Field(foreign_key="zoo.id")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Lion",
                    "species": "Panthera leo",
                    "image_filename": "https://example.com/lion.jpg",
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
    max_daily_checkout_hours: int | None = Field(default=None, nullable=True)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    zoo: Zoo = Relationship(back_populates="animals")
    events_link: list[AnimalEvent] = Relationship(back_populates="animal")
    activity_logs: list["AnimalActitvityLog"] = Relationship(back_populates="animal")
    audits: list["AnimalAudit"] = Relationship(back_populates="animal")
    health_logs: list["AnimalHealthLog"] = Relationship(back_populates="animal")


class EventTypeIn(SQLModel):
    name: str
    zoo_id: int = Field(foreign_key="zoo.id")
    group_id: int | None = Field(foreign_key="group.id", default=None)


class EventType(EventTypeIn, table=True):
    __tablename__ = "event_type"  # type: ignore

    id: int = Field(primary_key=True)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    zoo: Zoo = Relationship(back_populates="event_types")
    group: Group = Relationship(back_populates="event_types")
    events: list["Event"] = Relationship(back_populates="event_type")

    __table_args__ = (
        Index(
            "ix_unique_name_zoo_id_group_id", "name", "zoo_id", "group_id", unique=True
        ),
    )


class EventIn(SQLModel):
    name: str
    description: str
    start_at: datetime = Field(
        sa_column=sa.Column(
            type_=TIMESTAMP(timezone=True),
        )
    )
    end_at: datetime = Field(
        sa_column=sa.Column(
            type_=TIMESTAMP(timezone=True),
        )
    )
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
    comments: list["EventComment"] = Relationship(back_populates="event")
    users_link: list["UserEvent"] = Relationship(back_populates="event")


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
    changed_field: str | None = Field(default=None)
    old_value: str | None = Field(default=None)
    new_value: str | None = Field(default=None)
    description: str | None = Field(default=None)
    action: str

    changed_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=sa.Column(
            type_=TIMESTAMP(timezone=True),
        ),
    )
    changed_by: int = Field(foreign_key="user.id")

    user: User = Relationship(
        back_populates="audits", sa_relationship_kwargs={"lazy": "joined"}
    )
    animal: Animal = Relationship(
        back_populates="audits", sa_relationship_kwargs={"lazy": "joined"}
    )


class AnimalHealthLogIn(SQLModel):
    details: str


class AnimalHealthLog(SQLModel, table=True):
    __tablename__ = "animal_health_log"  # type: ignore

    id: int = Field(primary_key=True)
    animal_id: int = Field(foreign_key="animal.id")
    details: str
    logged_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=sa.Column(
            type_=TIMESTAMP(timezone=True),
        ),
    )
    logged_by: int = Field(foreign_key="user.id")

    animal: Animal = Relationship(
        back_populates="health_logs", sa_relationship_kwargs={"lazy": "joined"}
    )
    user: User = Relationship(
        back_populates="health_logs", sa_relationship_kwargs={"lazy": "joined"}
    )


class EventCommentIn(SQLModel):
    comment: str


class EventComment(EventCommentIn, table=True):
    __table_name__ = "event_comment"  # type: ignore

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    event_id: int | None = Field(foreign_key="event.id", default=None)

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    user: User = Relationship(back_populates="comments")
    event: Event = Relationship(back_populates="comments")


class UserEvent(SQLModel, table=True):
    __tablename__ = "user_event"  # type: ignore

    id: int = Field(primary_key=True)

    user_id: int | None = Field(default=None, foreign_key="user.id")
    event_id: int | None = Field(default=None, foreign_key="event.id")

    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()

    assigner_id: int | None

    user: User = Relationship(back_populates="events_link")
    event: Event = Relationship(back_populates="users_link")


# Composite models
class EventWithAnimals(BaseModel):
    event: Event
    animals: list[Animal]


class GroupWithMembers(BaseModel):
    group: GroupWithZoo
    members: list[UserPublic]


class EventCreate(BaseModel):
    event: EventIn
    animal_ids: list[int]
    user_ids: list[int]
    checkout_immediately: bool = False


class EventWithDetails(BaseModel):
    event: Event
    animals: list[Animal]
    users: list[UserPublic]
    event_type: EventType
    zoo: Zoo


class UserEventWithDetails(BaseModel):
    user_event: UserEvent
    user: UserPublic


class AnimalEventWithDetails(BaseModel):
    animal_event: AnimalEvent
    animal: Animal


class EventCommentWithUser(BaseModel):
    comment: EventComment
    user: UserPublic


class EventWithDetailsAndComments(BaseModel):
    event: Event
    animals: list[AnimalEventWithDetails]
    users: list[UserEventWithDetails]
    event_type: EventType
    zoo: Zoo
    comments: list[EventCommentWithUser]


class AnimalWithCurrentEvent(BaseModel):
    animal: Animal
    current_event: EventWithDetailsAndComments


class AnimalWithEvents(BaseModel):
    animal: Animal
    upcoming_events: list[EventWithDetailsAndComments]
    current_events: list[EventWithDetailsAndComments]
    past_events: list[EventWithDetailsAndComments]
    zoo: Zoo
    daily_checkout_count: int
    daily_checkout_duration: float
    weekly_event_activity_hours: float


class UserWithEvents(BaseModel):
    user: UserWithDetails
    upcoming_events: list[EventWithDetailsAndComments]
    current_events: list[EventWithDetailsAndComments]
    past_events: list[EventWithDetailsAndComments]


class AnimalStatus(BaseModel):
    animal: Animal
    status: Literal["available", "checked_out", "unavailable"]
    status_description: str
    daily_event_count: int
    daily_event_duration: float


class AnimalAuditWithDetails(BaseModel):
    user: UserPublic
    audit: AnimalAudit
    animal: Animal


class AnimalHealthLogWithDetails(BaseModel):
    user: UserPublic
    log: AnimalHealthLog
    animal: Animal


class RestingAnimal(BaseModel):
    animal_status: AnimalStatus
    daily_checkout_count: int
    weekly_event_activity_hours: float
    daily_checkout_duration: float
    health_logs: list[AnimalHealthLogWithDetails]


class FeedEvent(BaseModel):
    name: str
    image: str | None
    description: str
    logged_at: datetime
    by: str

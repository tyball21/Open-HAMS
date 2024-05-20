from fastapi import APIRouter, HTTPException
from sqlmodel import select

from api.deps import CurrentUser, SessionDep
from db.utils import has_permission
from models import EventType, EventTypeIn

router = APIRouter(prefix="/events-types", tags=["Events", "Events Types"])


@router.get("/")
async def read_all_events_types(session: SessionDep) -> list[EventType]:
    event_types = await session.exec(select(EventType))
    return list(event_types.all())


@router.post("/")
async def create_event_type(
    event: EventTypeIn,
    session: SessionDep,
    current_user: CurrentUser,
) -> EventType:
    if not has_permission(current_user.role.permissions, "manage_events"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    event = EventType(**event.model_dump())
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event

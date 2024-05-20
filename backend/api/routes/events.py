from datetime import UTC, datetime

from api.deps import CurrentUser, SessionDep
from db.animals import log_activity, log_audit
from db.events import get_all_events
from db.utils import has_permission
from fastapi import APIRouter, Body, HTTPException
from models import (
    Animal,
    AnimalActitvityLog,
    AnimalEvent,
    Event,
    EventIn,
    EventWithAnimals,
)
from sqlmodel import col, select

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/")
async def read_all_events(session: SessionDep) -> list[Event]:
    return await get_all_events(session)


@router.post("/")
async def create_event(
    event: EventIn, session: SessionDep, current_user: CurrentUser
) -> Event:
    if not has_permission(current_user.role.permissions, "manage_events"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    event = Event(**event.model_dump())
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


@router.get("/{event_id}")
async def read_event(event_id: int, session: SessionDep) -> Event:
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{event_id}")
async def update_event(
    event_id: int,
    event_update: EventIn,
    session: SessionDep,
    current_user: CurrentUser,
) -> Event:
    if not has_permission(current_user.role.permissions, "manage_events"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    for field, value in event_update.model_dump().items():
        setattr(event, field, value)

    await session.commit()
    await session.refresh(event)
    return event


@router.post("/{event_id}/assign-animals")
async def assign_animals_to_event(
    event_id: int,
    session: SessionDep,
    current_user: CurrentUser,
    animal_ids: list[int] = Body(...),
):
    if not has_permission(current_user.role.permissions, "manage_events"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    event = await session.get(Event, event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    animals = await session.exec(select(Animal).where(col(Animal.id).in_(animal_ids)))
    animals = animals.all()

    if not animals:
        raise HTTPException(status_code=404, detail="No animals found")

    for animal in animals:
        # create a link between the animal and the event
        event_animal_link = AnimalEvent(animal_id=animal.id, event_id=event_id)  # type: ignore
        session.add(event_animal_link)

        # log the activity
        log = f"Animal {animal.id} assigned to event {event_id}"
        await log_activity(animal.id, log, session)

    session.add(event)
    await session.commit()
    await session.refresh(event)

    return event


@router.post("/{event_id}/remove-animals")
async def remove_animals_from_event(
    event_id: int,
    session: SessionDep,
    current_user: CurrentUser,
    animal_ids: list[int] = Body(...),
):
    if not has_permission(current_user.role.permissions, "manage_events"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    event = await session.get(Event, event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    animals = await session.exec(select(Animal).where(col(Animal.id).in_(animal_ids)))
    animals = animals.all()

    if not animals:
        raise HTTPException(status_code=404, detail="No animals found")

    for animal in animals:
        # remove the link between the animal and the event
        event_animal_link = await session.exec(
            select(AnimalEvent).where(
                AnimalEvent.animal_id == animal.id, AnimalEvent.event_id == event_id
            )
        )
        event_animal_link = event_animal_link.first()

        if not event_animal_link:
            continue

        await session.delete(event_animal_link)

        # log the activity
        log = f"Animal {animal.id} removed from event {event_id}"
        await log_activity(animal.id, log, session)

    session.add(event)
    await session.commit()
    await session.refresh(event)

    return event


@router.get("/{event_id}/animals")
async def get_event_animals(event_id: int, session: SessionDep) -> EventWithAnimals:
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    animals = await session.exec(
        select(Animal).join(AnimalEvent).where(AnimalEvent.event_id == event_id)
    )
    animals = animals.all()

    return EventWithAnimals(event=event, animals=animals)


@router.post("/{event_id}/animal/{animal_id}/check-in")
async def check_in_animal(
    event_id: int, animal_id: int, session: SessionDep, current_user: CurrentUser
):
    """
    Check in an animal to an event and update the animal's daily checkout count
    """

    if not has_permission(current_user.role.permissions, "checkout_animals"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    animal = await session.get(Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    # check if users has enough tier to check in the animal
    if current_user.tier < animal.tier:
        raise HTTPException(
            status_code=401,
            detail="Users does not have enough tier to check in/out this animal",
        )

    event_animal_link = await session.exec(
        select(AnimalEvent).where(
            AnimalEvent.animal_id == animal_id, AnimalEvent.event_id == event_id
        )
    )
    event_animal_link = event_animal_link.first()

    if not animal.checked_in:
        raise HTTPException(
            status_code=400, detail="Animal is already checked in to some event"
        )

    if not event_animal_link:
        raise HTTPException(status_code=404, detail="Animal not assigned to this event")

    if event_animal_link.checked_in:
        raise HTTPException(
            status_code=400, detail="Animal is already checked in to event"
        )

    if animal.daily_checkout_count >= animal.max_daily_checkouts:
        raise HTTPException(
            status_code=400, detail="Animal has reached maximum checkouts for the day"
        )

    event_duration = event.end_at - event.start_at
    possible_animal_checkout_duration = animal.daily_checkout_duration + event_duration
    possible_animal_hours = possible_animal_checkout_duration.total_seconds() / 3600
    if possible_animal_hours > float(animal.max_daily_checkout_hours):
        raise HTTPException(
            status_code=400,
            detail="Animal has reached maximum checkout hours for the day",
        )

    animal.daily_checkout_count += 1
    animal.checked_in = False

    event_animal_link.checked_in = datetime.now(UTC)
    event_animal_link.user_in_id = current_user.id

    # log the activity
    log = f"Animal {animal_id} checked in to event {event_id}"
    await log_activity(animal_id, log, session)

    # log the audit
    await log_audit(
        animal.id, current_user.id, "status", "checked_in", "checked_out", session
    )

    session.add(event_animal_link)
    await session.commit()

    return {"message": "Animal checked in"}


@router.post("/{event_id}/animal/{animal_id}/check-out")
async def check_out_animal(
    event_id: int, animal_id: int, session: SessionDep, current_user: CurrentUser
):
    if not has_permission(current_user.role.permissions, "checkout_animals"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    animal = await session.get(Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    # check if users has enough tier to check in the animal
    if current_user.tier < animal.tier:
        raise HTTPException(
            status_code=401,
            detail="Users does not have enough tier to check in/out this animal",
        )

    event_animal_link = await session.exec(
        select(AnimalEvent).where(
            AnimalEvent.animal_id == animal_id, AnimalEvent.event_id == event_id
        )
    )
    event_animal_link = event_animal_link.first()

    if animal.checked_in:
        raise HTTPException(
            status_code=400, detail="Animal is not checked in to any event"
        )

    if not event_animal_link:
        raise HTTPException(status_code=404, detail="Animal not assigned to this event")

    if not event_animal_link.checked_in:
        raise HTTPException(status_code=400, detail="Animal is not checked in")

    if event_animal_link.checked_out:
        raise HTTPException(status_code=400, detail="Animal is already checked out")

    event_animal_link.checked_out = datetime.now(UTC)
    event_animal_link.user_out_id = current_user.id
    event_animal_link.duration = (
        event_animal_link.checked_out - event_animal_link.checked_in
    )

    animal.checked_in = True
    animal.daily_checkout_duration += event_animal_link.duration

    # log the activity
    log = f"Animal {animal_id} checked out from event {event_id}"
    await log_activity(animal_id, log, session)

    # log the audit
    await log_audit(
        animal.id, current_user.id, "status", "checked_out", "checked_in", session
    )

    session.add(event_animal_link)
    session.add(animal)
    await session.commit()

    return {"message": "Animal checked out"}

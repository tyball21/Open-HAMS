from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlmodel import and_, col, select

from api.deps import CurrentUser, SessionDep
from db.animals import (
    log_audit,
    update_animals_status,
    validate_animals,
    validate_animals_availability,
    validate_event_clashes,
    validate_tiers,
)
from db.events import get_events_details
from db.permissions import has_permission
from db.users import validate_check_in_out_permissions, validate_users
from models import (
    Animal,
    AnimalEvent,
    Event,
    EventComment,
    EventCommentIn,
    EventCreate,
    EventType,
    EventWithDetails,
    EventWithDetailsAndComments,
    Role,
    User,
    UserEvent,
)

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/")
async def read_all_events(session: SessionDep, details: bool = True):
    if details:
        query = (
            select(
                Event,
                EventType,
                func.count(col(AnimalEvent.animal_id)).label("animal_count"),
            )
            .join(AnimalEvent, isouter=True)
            .join(EventType)
            .group_by(col(Event.id), col(EventType.id))
        )
        events = (await session.exec(query)).all()
        return [
            {"event": event, "animal_count": animal_count, "event_type": event_type}
            for event, event_type, animal_count in events
        ]

    query = select(Event)
    events = (await session.exec(query)).all()
    return events


@router.get("/details")
async def get_events_details_by_date(
    session: SessionDep,
    id: int = Query(..., description="Event ID to filter events"),
) -> EventWithDetailsAndComments:
    query = (
        select(
            Event,
        )
        .where(Event.id == id)
        .options(
            joinedload(Event.event_type),  # type: ignore
            joinedload(Event.zoo),  # type: ignore
        )
    )
    events = list((await session.exec(query)).all())
    return (await get_events_details(session, events))[0]


class GetUpcomingLiveEvents(BaseModel):
    live: list[EventWithDetailsAndComments]
    upcoming: list[EventWithDetailsAndComments]


@router.get("/details/upcoming-live")
async def get_upcoming_live_events(
    session: SessionDep,
) -> GetUpcomingLiveEvents:
    now = datetime.now(UTC)
    query = (
        select(
            Event,
        )
        .where(Event.end_at > now)
        .options(
            joinedload(Event.event_type),  # type: ignore
            joinedload(Event.zoo),  # type: ignore
        )
    )
    events = list((await session.exec(query)).all())
    events_details = await get_events_details(session, events)

    live, upcoming = [], []
    for event in events_details:
        if event.event.start_at <= now <= event.event.end_at:
            live.append(event)
        else:
            upcoming.append(event)

    return GetUpcomingLiveEvents(live=live, upcoming=upcoming)


@router.post("/")
async def create_event(
    body: EventCreate, session: SessionDep, current_user: CurrentUser
):
    if not has_permission(current_user.role.permissions, "create_events"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    # validate event type
    event_type = await session.exec(
        select(EventType.id).where(
            and_(
                EventType.id == body.event.event_type_id,
                EventType.zoo_id == body.event.zoo_id,
            )
        )
    )
    if not event_type.first():
        raise HTTPException(status_code=404, detail="Event type not found for this zoo")

    # validate users
    users = await session.exec(select(User).where(col(User.id).in_(body.user_ids)))
    users = list(users.unique())
    if len(users) != len(body.user_ids):
        raise HTTPException(status_code=404, detail="User not found")

    # validate animals
    animals = await validate_animals(
        body.animal_ids, zoo_id=body.event.zoo_id, session=session
    )

    # check if animals are already assigned to an event during this time
    await validate_event_clashes(
        body.animal_ids,
        body.event.end_at,
        body.event.start_at,
        body.event.zoo_id,
        session,
    )

    # validate checkouts if checkout_immediately
    if body.checkout_immediately:
        # Only validate for immediate checkout if the event is starting now,
        # not for future events that are set to auto-checkout.
        now = datetime.now(UTC)
        if not body.event.start_at > now:
            await validate_tiers(animals, current_user)
            await validate_animals_availability(body.animal_ids, session)

    event = Event(**body.event.model_dump())
    session.add(event)

    current_user_id = current_user.id

    await session.commit()
    await session.refresh(event)

    for id in body.user_ids:
        user_link = UserEvent(
            user_id=id, event_id=event.id, assigner_id=current_user_id
        )  # type: ignore
        session.add(user_link)

    now = datetime.now(UTC)
    for id in body.animal_ids:
        animal_link = AnimalEvent(
            animal_id=id,
            event_id=event.id,
            checked_out=now if body.checkout_immediately else None,
            user_out_id=current_user_id if body.checkout_immediately else None,
        )  # type: ignore
        session.add(animal_link)

    await session.commit()

    # update animals status
    if body.checkout_immediately:
        await update_animals_status(body.animal_ids, "checked_out", session)

    # refresh event
    await session.refresh(event)
    await session.refresh(current_user)

    # create audit logs for animals assignment
    if body.animal_ids:
        for animal_id in body.animal_ids:
            await log_audit(
                session=session,
                animal_id=animal_id,
                changed_by=current_user.id,
                action="event_participation_added",
                commit=False,
                description=f"{current_user.first_name} {current_user.last_name} ({current_user.role.name}) added animal to event '{event.name}'",
            )

    # create audit logs for animal checkout
    if body.checkout_immediately:
        for animal_id in body.animal_ids:
            await log_audit(
                session=session,
                animal_id=animal_id,
                changed_by=current_user.id,
                action="checked_out",
                commit=False,
                description=f"{current_user.first_name} {current_user.last_name} ({current_user.role.name}) checked out animal to event '{event.name}'",
            )

    await session.commit()
    await session.refresh(event)

    return JSONResponse({"message": "Event created"}, status_code=200)


@router.put("/{event_id}")
async def update_event(
    body: EventCreate, session: SessionDep, current_user: CurrentUser, event_id: int
):
    if not has_permission(current_user.role.permissions, "update_events"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # if event is already started, then it start time can't be changed
    if event.start_at < datetime.now(UTC):
        if event.start_at != body.event.start_at:
            raise HTTPException(
                status_code=400, detail="Event start time can't be changed"
            )

    # if event is ended, then it can't be updated
    if event.end_at < datetime.now(UTC):
        raise HTTPException(status_code=400, detail="Event is already ended")

    # validate event type
    event_type = await session.exec(
        select(EventType.id).where(
            and_(
                EventType.id == body.event.event_type_id,
                EventType.zoo_id == body.event.zoo_id,
            )
        )
    )
    if not event_type.first():
        raise HTTPException(status_code=404, detail="Event type not found for this zoo")

    # validate users
    await validate_users(body.user_ids, session)

    # validate animals
    await validate_animals(body.animal_ids, zoo_id=body.event.zoo_id, session=session)

    # check if animals are already assigned to an event during this time
    await validate_event_clashes(
        body.animal_ids,
        body.event.end_at,
        body.event.start_at,
        body.event.zoo_id,
        session,
        event_id=event_id,
    )

    for k, v in body.event.model_dump().items():
        setattr(event, k, v)

    # existing_users
    existing_users = await session.exec(
        select(UserEvent).where(UserEvent.event_id == event_id)
    )
    existing_users = list(existing_users.all())

    # existing_animals
    existing_animals = await session.exec(
        select(AnimalEvent).where(AnimalEvent.event_id == event_id)
    )
    existing_animals = list(existing_animals.all())

    # to remove users
    to_remove_users = [
        user for user in existing_users if user.user_id not in body.user_ids
    ]
    for user in to_remove_users:
        await session.delete(user)

    # to remove animals
    to_remove_animals = [
        animal for animal in existing_animals if animal.animal_id not in body.animal_ids
    ]
    for animal in to_remove_animals:
        if animal.checked_out:
            raise HTTPException(
                status_code=400,
                detail=f"{animal.animal.name} is already checked out, can't be removed",
            )
        await session.delete(animal)

    # to add users
    to_add_users = [
        user
        for user in body.user_ids
        if user not in [user.user_id for user in existing_users]
    ]
    for user in to_add_users:
        user_link = UserEvent(
            user_id=user,
            event_id=event_id,
            assigner_id=current_user.id,  # type: ignore
        )
        session.add(user_link)

    # to add animals
    to_add_animals = [
        animal
        for animal in body.animal_ids
        if animal not in [animal.animal_id for animal in existing_animals]
    ]
    for animal in to_add_animals:
        animal_link = AnimalEvent(animal_id=animal, event_id=event_id)  # type: ignore
        session.add(animal_link)

    # audit logs
    for animal in to_remove_animals:
        await log_audit(
            session=session,
            animal_id=animal.animal_id,
            changed_by=current_user.id,
            action="event_participation_removed",
            commit=False,
            description=f"{current_user.first_name} {current_user.last_name} ({current_user.role.name}) removed animal from event '{event.name}'",
        )

    for animal in to_add_animals:
        await log_audit(
            session=session,
            animal_id=animal,
            changed_by=current_user.id,
            action="event_participation_added",
            commit=False,
            description=f"{current_user.first_name} {current_user.last_name} ({current_user.role.name}) added animal to event '{event.name}'",
        )

    await session.commit()
    await session.refresh(event)

    return JSONResponse({"message": "Event updated"}, status_code=200)


@router.delete("/{event_id}")
async def delete_event(event_id: int, session: SessionDep, current_user: CurrentUser):
    if not has_permission(current_user.role.permissions, "delete_events"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check if any animals are currently checked out for this event
    animal_links = await session.exec(
        select(AnimalEvent).where(
            AnimalEvent.event_id == event_id,
            AnimalEvent.checked_out.is_not(None),  # Animals that have been checked out
            AnimalEvent.checked_in.is_(None)       # But not yet checked in
        ).options(joinedload(AnimalEvent.animal))  # type: ignore
    )
    animal_links = list(animal_links.all())  # type: ignore
    
    # Auto check-in any animals that are currently checked out
    if animal_links:
        # Get list of animal IDs to check in
        checked_out_animal_ids = [animal_link.animal_id for animal_link in animal_links]
        
        # Mark animals as checked in
        now = datetime.now(UTC)
        for animal_link in animal_links:
            animal_link.checked_in = now
            animal_link.user_in_id = current_user.id
            animal_link.duration = now - animal_link.checked_out  # type: ignore
            session.add(animal_link)
        
        # Update animals status to checked_in
        await update_animals_status(checked_out_animal_ids, "checked_in", session)
        
        # Create audit logs for auto check-in
        for animal_id in checked_out_animal_ids:
            # Audit log for auto check-in
            await log_audit(
                session=session,
                animal_id=animal_id,
                changed_by=current_user.id,
                action="checked_in",
                commit=False,
                description=f"Animal automatically checked in due to event deletion of '{event.name}'",
            )

            # Audit log for status change
            await log_audit(
                session=session,
                animal_id=animal_id,
                changed_by=current_user.id,
                action="animal_status_changed",
                commit=False,
                changed_field="status",
                old_value="checked_out",
                new_value="checked_in",
                description=f"Animal status changed due to automatic check-in from event deletion of '{event.name}'",
            )
        
        await session.commit()

    # delete all user links
    user_links = await session.exec(
        select(UserEvent).where(UserEvent.event_id == event_id)
    )
    for user_link in user_links:
        await session.delete(user_link)

    # delete all animal links
    all_animal_links = await session.exec(
        select(AnimalEvent).where(AnimalEvent.event_id == event_id)
    )
    for animal_link in all_animal_links:
        await session.delete(animal_link)

    await session.delete(event)
    await session.commit()

    return {"message": "Event deleted"}


@router.get("/{event_id}")
async def read_event(event_id: int, session: SessionDep) -> EventWithDetails:
    event = await session.exec(
        select(Event)
        .where(Event.id == event_id)
        .options(joinedload(Event.event_type), joinedload(Event.zoo))  # type: ignore
    )
    event = event.first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    handlers = await session.exec(
        select(User).join(UserEvent).where(UserEvent.event_id == event_id)
    )
    handlers = list(handlers.unique())

    animals = await session.exec(
        select(Animal).join(AnimalEvent).where(AnimalEvent.event_id == event_id)
    )
    animals = list(animals.unique())

    return EventWithDetails(
        event=event,
        event_type=event.event_type,
        zoo=event.zoo,
        users=handlers,  # type: ignore
        animals=animals,
    )


class AssignAnimalsIn(BaseModel):
    animal_ids: list[int]


@router.put("/{event_id}/animals")
async def reassign_animals_to_event(
    event_id: int,
    session: SessionDep,
    current_user: CurrentUser,
    body: AssignAnimalsIn,
):
    if not has_permission(current_user.role.permissions, "update_events"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    event = await session.get(Event, event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    await validate_animals(body.animal_ids, session)

    # check if animals are already assigned to an event during this time
    clashing_animals = await session.exec(
        select(Animal.name)
        .join(AnimalEvent)
        .join(Event)
        .where(
            and_(
                Event.start_at <= event.end_at,
                Event.end_at >= event.start_at,
                Event.zoo_id == event.zoo_id,
                col(Animal.id).in_(body.animal_ids),
                Event.id != event_id,
            )
        )
        .group_by(Animal.name)
    )
    clashing_animals = clashing_animals.all()
    if clashing_animals:
        raise HTTPException(
            status_code=400,
            detail=f'Some animals are already assigned to an event during this time: {", ".join([animal for animal in clashing_animals])}',
        )

    # already assigned animals
    assigned_animals = await session.exec(
        select(Animal).join(AnimalEvent).where(AnimalEvent.event_id == event_id)
    )
    assigned_animals = assigned_animals.all()

    # to remove animals
    to_remove_animal_ids = [
        animal.id for animal in assigned_animals if animal.id not in body.animal_ids
    ]

    for animal_id in to_remove_animal_ids:
        event_animal_link = await session.exec(
            select(AnimalEvent).where(
                AnimalEvent.animal_id == animal_id, AnimalEvent.event_id == event_id
            )
        )
        event_animal_link = event_animal_link.first()
        await session.delete(event_animal_link)

    # to add animals
    to_add_animal_ids = [
        animal_id
        for animal_id in body.animal_ids
        if animal_id not in [animal.id for animal in assigned_animals]
    ]

    for animal_id in to_add_animal_ids:
        animal_link = AnimalEvent(animal_id=animal_id, event_id=event_id)  # type: ignore
        session.add(animal_link)

    # audit logs
    for animal in to_remove_animal_ids:
        await log_audit(
            session=session,
            animal_id=animal,
            changed_by=current_user.id,
            action="event_participation_removed",
            commit=False,
            description=f"{current_user.first_name} {current_user.last_name} ({current_user.role.name}) removed animal from event '{event.name}'",
        )

    for animal in to_remove_animal_ids:
        await log_audit(
            session=session,
            animal_id=animal,
            changed_by=current_user.id,
            action="event_participation_added",
            commit=False,
            description=f"{current_user.first_name} {current_user.last_name} ({current_user.role.name}) added animal to event '{event.name}'",
        )

    await session.commit()
    await session.refresh(event)

    return {"message": "Changes saved"}


class AssignHandlersIn(BaseModel):
    handler_ids: list[int]


@router.put("/{event_id}/handlers")
async def reassign_handlers_to_event(
    event_id: int,
    session: SessionDep,
    current_user: CurrentUser,
    body: AssignHandlersIn,
):
    if not has_permission(current_user.role.permissions, "update_events"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    handler_role = await session.exec(select(Role).where(Role.name == "handler"))
    handler_role = handler_role.first()

    if not handler_role:
        raise HTTPException(status_code=404, detail="Handler role not found")

    handlers = await session.exec(
        select(User).where(
            col(User.id).in_(body.handler_ids), User.role_id == handler_role.id
        )
    )
    handlers = list(handlers.all())

    if not (len(handlers) == len(body.handler_ids)):
        raise HTTPException(status_code=404, detail="Handler not found")

    current_handlers = await session.exec(
        select(User).join(UserEvent).where(UserEvent.event_id == event_id)
    )
    current_handlers = list(current_handlers.all())

    # to remove handlers
    to_remove_handler_ids = [
        handler.id for handler in current_handlers if handler.id not in body.handler_ids
    ]

    for handler_id in to_remove_handler_ids:
        link = await session.exec(
            select(UserEvent).where(
                UserEvent.user_id == handler_id, UserEvent.event_id == event_id
            )
        )
        link = link.first()
        await session.delete(link)
        await session.commit()

    # to add handlers
    to_add_handler_ids = [
        handler_id
        for handler_id in body.handler_ids
        if handler_id not in [handler.id for handler in current_handlers]
    ]

    for handler_id in to_add_handler_ids:
        user_link = UserEvent(
            user_id=handler_id,
            event_id=event_id,
            assigner_id=current_user.id,  # type: ignore
        )  # type: ignore
        session.add(user_link)

    await session.commit()
    await session.refresh(event)

    return {"message": "Changes saved"}


@router.post("/{event_id}/comments")
async def add_comment_to_event(
    event_id: int,
    body: EventCommentIn,
    session: SessionDep,
    current_user: CurrentUser,
):
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    comment = EventComment(
        event_id=event_id,
        user_id=current_user.id,
        comment=body.comment,
    )  # type: ignore

    session.add(comment)
    await session.commit()

    return JSONResponse({"message": "Comment added"}, status_code=200)


class AnimalCheckInOut(BaseModel):
    animal_ids: list[int]


@router.put("/{event_id}/checkin")
async def checkin_animal(
    event_id: int,
    body: AnimalCheckInOut,
    session: SessionDep,
    current_user: CurrentUser,
):
    if not await validate_check_in_out_permissions(current_user, event_id, session):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    # validate event
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # validate that animals are assigned to this event
    animals_link: list[AnimalEvent] = await session.exec(
        select(AnimalEvent)
        .where(
            col(AnimalEvent.event_id) == event_id,
            col(AnimalEvent.animal_id).in_(body.animal_ids),
        )
        .options(joinedload(AnimalEvent.animal))  # type: ignore
    )
    animals_link = list(animals_link.all())  # type: ignore
    animals = [animal_link.animal for animal_link in animals_link]

    if not len(animals) == len(body.animal_ids):
        raise HTTPException(
            status_code=404, detail="Some animals are not assigned to this event"
        )

    # check if already checked in or not checked out
    for animal_link in animals_link:
        if animal_link.checked_in:
            raise HTTPException(
                status_code=400,
                detail=f"Animal {animal_link.animal.name} is already checked in",
            )

        if not animal_link.checked_out:
            raise HTTPException(
                status_code=400,
                detail=f"Animal {animal_link.animal.name} is not checked out for this event",
            )

    # validate animals and user tier
    await validate_tiers(animals, current_user)

    # finally checkin animals
    for animal_link in animals_link:
        now = datetime.now(UTC)
        animal_link.checked_in = now
        animal_link.user_in_id = current_user.id
        animal_link.duration = now - animal_link.checked_out  # type: ignore
        session.add(animal_link)

    await session.commit()
    await session.refresh(event)

    # update animals status and audit logs
    await update_animals_status(body.animal_ids, "checked_in", session)

    # refresh event and user
    await session.refresh(event)
    await session.refresh(current_user)

    # create audit logs for animals assignment and animal status change
    for animal_id in body.animal_ids:
        # audit log for checkin
        await log_audit(
            session=session,
            animal_id=animal_id,
            changed_by=current_user.id,
            action="checked_in",
            commit=False,
            description=f"{current_user.first_name} {current_user.last_name} ({current_user.role.name}) checked in animal to event '{event.name}'",
        )

        # audit log for animal status change
        await log_audit(
            session=session,
            animal_id=animal_id,
            changed_by=current_user.id,
            action="animal_status_changed",
            commit=False,
            changed_field="status",
            old_value="checked_out",
            new_value="checked_in",
            description=f"{current_user.first_name} {current_user.last_name} ({current_user.role.name}) checked in animal to event '{event.name}'",
        )

        # audit log for rest time start
        await log_audit(
            session=session,
            animal_id=animal_id,
            changed_by=current_user.id,
            action="rest_time_started",
            commit=False,
            description="Rest time started",
        )

    await session.commit()
    await session.refresh(event)

    return {"message": "Animals checked in"}


@router.put("/{event_id}/checkout")
async def checkout_animal(
    event_id: int,
    body: AnimalCheckInOut,
    session: SessionDep,
    current_user: CurrentUser,
):
    if not await validate_check_in_out_permissions(current_user, event_id, session):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    # validate event
    event = await session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # validate animals avaialability
    await validate_animals_availability(body.animal_ids, session)

    # validate that animals are assigned to this event
    animals_link: list[AnimalEvent] = await session.exec(
        select(AnimalEvent)
        .where(
            col(AnimalEvent.event_id) == event_id,
            col(AnimalEvent.animal_id).in_(body.animal_ids),
        )
        .options(joinedload(AnimalEvent.animal))  # type: ignore
    )
    animals_link = list(animals_link.all())  # type: ignore
    animals = [animal_link.animal for animal_link in animals_link]

    if not len(animals_link) == len(body.animal_ids):
        raise HTTPException(
            status_code=404, detail="Some animals are not assigned to this event"
        )

    # check if already checked out
    for animal_link in animals_link:
        # if already checked out
        if animal_link.checked_out:
            raise HTTPException(
                status_code=400,
                detail=f"Animal {animal_link.animal.name} is already checked out",
            )

    # validate animals and user tier
    await validate_tiers(animals, current_user)

    # finally checkout animals
    for animal_link in animals_link:
        animal_link.checked_out = datetime.now(UTC)
        animal_link.user_out_id = current_user.id
        session.add(animal_link)

    await session.commit()
    await session.refresh(event)

    # update animals status
    await update_animals_status(body.animal_ids, "checked_out", session)

    # refresh event
    await session.refresh(event)
    await session.refresh(current_user)

    # create audit logs for animals assignment
    for animal_id in body.animal_ids:
        # audit log for checkout
        await log_audit(
            session=session,
            animal_id=animal_id,
            changed_by=current_user.id,
            action="checked_out",
            commit=False,
            description=f"{current_user.first_name} {current_user.last_name} ({current_user.role.name}) checked out animal to event '{event.name}'",
        )

        # audit log for animal status change
        await log_audit(
            session=session,
            animal_id=animal_id,
            changed_by=current_user.id,
            action="animal_status_changed",
            commit=False,
            changed_field="status",
            old_value="checked_in",
            new_value="checked_out",
            description=f"{current_user.first_name} {current_user.last_name} ({current_user.role.name}) checked out animal to event '{event.name}'",
        )

    await session.commit()
    await session.refresh(event)

    return {"message": "Animals checked out"}

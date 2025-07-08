from datetime import UTC, date, datetime, timedelta
from pathlib import Path
import shutil
import uuid

from fastapi import APIRouter, HTTPException, Form, UploadFile, File, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlmodel import and_, col, desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_current_user, get_db_session
from core.utils import snake_to_capital_case
from db.animals import (
    get_all_animals,
    get_animal_by_id,
    get_animals_status,
    log_audit,
    log_fields_update,
    retrieve_animal_logs,
    toggle_animal_availability,
)
from db.events import get_events_details
from db.permissions import has_permission
from models import (
    Animal,
    AnimalAudit,
    AnimalAuditWithDetails,
    AnimalEvent,
    AnimalEventWithDetails,
    AnimalHealthLog,
    AnimalHealthLogIn,
    AnimalHealthLogWithDetails,
    AnimalIn,
    AnimalWithCurrentEvent,
    AnimalWithEvents,
    Event,
    EventComment,
    EventCommentWithUser,
    EventWithDetailsAndComments,
    FeedEvent,
    RestingAnimal,
    User,
    UserEvent,
    UserEventWithDetails,
    Zoo,
)

IMAGE_DIR = Path("static/animal_images") # Define the directory for animal images

router = APIRouter(prefix="/animals", tags=["Animals"])


def parse_form_boolean(value: str | bool) -> bool:
    """Convert FormData boolean string to actual boolean"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'on')
    return False


def parse_form_int(value: str | int | None) -> int | None:
    """Convert FormData string to int, handling None and empty strings"""
    if value is None or value == '':
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return None
    return None


def parse_form_float(value: str | float | None) -> float | None:
    """Convert FormData string to float, handling None and empty strings"""
    if value is None or value == '':
        return None
    if isinstance(value, float):
        return value
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


@router.get("/")
async def read_all_animals(
    session: AsyncSession = Depends(get_db_session), zoo_id: int | None = None
) -> list[Animal]:
    return await get_all_animals(zoo_id, session)


@router.get("/status")
async def get_animal_status(session: AsyncSession = Depends(get_db_session), zoo_id: int | None = None):
    return await get_animals_status(session, zoo_id=zoo_id)


@router.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_db_session)) -> list[FeedEvent]:
    req_actions = [
        "checked_in",
        "checked_out",
        "comment_added",
        "comment_updated",
        "health_log_added",
        "health_log_updated",
    ]

    feed = await session.exec(
        select(AnimalAudit)
        .where(col(AnimalAudit.action).in_(req_actions))
        .order_by(desc(AnimalAudit.changed_at))
    )
    feed = list(feed.unique())
    feed_list: list[FeedEvent] = []

    for item in feed:
        event = FeedEvent(
            name=item.animal.name,
            description=snake_to_capital_case(item.action),
            image=item.animal.image_filename,
            logged_at=item.changed_at,
            by=f"{item.user.first_name} {item.user.last_name}",
        )
        feed_list.append(event)

    return feed_list


@router.get("/{animal_id}")
async def get_animal(animal_id: int, session: AsyncSession = Depends(get_db_session)) -> Animal:
    animal = await get_animal_by_id(animal_id, session)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


@router.get("/{animal_id}/details")
async def get_animal_details(animal_id: int, session: AsyncSession = Depends(get_db_session)) -> AnimalWithEvents:
    query = (
        select(
            Animal,
            func.count(col(AnimalEvent.id)).label("daily_event_count"),
            func.sum(col(AnimalEvent.duration)).label("daily_event_duration"),
        )
        .outerjoin(
            AnimalEvent,
            (
                and_(
                    col(Animal.id) == col(AnimalEvent.animal_id),
                    func.DATE(col(AnimalEvent.checked_in)) == date.today(),
                )
            ),
        )
        .where(Animal.id == animal_id)
        .group_by(col(Animal.id))
    )
    animal = (await session.exec(query)).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    animal, daily_event_count, daily_event_duration = animal

    zoo = await session.exec(select(Zoo).where(Zoo.id == animal.zoo_id))
    zoo = zoo.first()

    # convert to hours
    daily_event_duration = (
        daily_event_duration / timedelta(hours=1) if daily_event_duration else 0
    )

    # events
    events = await session.exec(
        select(Event).join(AnimalEvent).where(AnimalEvent.animal_id == animal_id)
    )
    events = events.all()

    event_ids = [event.id for event in events]
    print("event_ids", event_ids)
    event_animal_details: list[AnimalEvent] = await session.exec(
        select(AnimalEvent)
        .where(col(AnimalEvent.event_id).in_(event_ids))
        .options(
            joinedload(AnimalEvent.animal),  # type: ignore
        )
    )
    event_animal_details = list(event_animal_details.unique())  # type: ignore

    event_user_details = await session.exec(
        select(UserEvent)
        .where(col(UserEvent.event_id).in_(event_ids))
        .options(
            joinedload(UserEvent.user),  # type: ignore
        )
    )
    event_user_details = list(event_user_details.unique())

    events_comments = await session.exec(
        select(EventComment)
        .where(col(EventComment.event_id).in_(event_ids))
        .options(
            joinedload(EventComment.user)  # type: ignore
        )
    )
    events_comments = list(events_comments.unique())

    events_with_details: list[EventWithDetailsAndComments] = []
    for event in events:
        event_details = EventWithDetailsAndComments(
            event=event,
            animals=[
                AnimalEventWithDetails(
                    animal_event=animal_event, animal=animal_event.animal
                )
                for animal_event in event_animal_details
                if animal_event.event_id == event.id
            ],
            users=[
                UserEventWithDetails(user_event=user_event, user=user_event.user)
                for user_event in event_user_details
                if user_event.event_id == event.id
            ],
            comments=[
                EventCommentWithUser(user=event_comment.user, comment=event_comment)
                for event_comment in events_comments
                if event_comment.event_id == event.id
            ],
            event_type=event.event_type,
            zoo=event.zoo,
        )
        events_with_details.append(event_details)

    # separate events based on current, past, upcoming
    current_time = datetime.now(UTC)
    current_events = []
    past_events = []
    upcoming_events = []

    for event in events_with_details:
        if event.event.start_at <= current_time <= event.event.end_at:
            current_events.append(event)
        elif event.event.end_at < current_time:
            past_events.append(event)
        elif event.event.start_at > current_time:
            upcoming_events.append(event)

    # calculate weekly activity (total duration of events in a week)
    weekly_event_activity = sum(
        (event.duration for event in event_animal_details if event.duration),
        timedelta(0),
    )

    return AnimalWithEvents(
        animal=animal,
        current_events=current_events,
        past_events=past_events,
        upcoming_events=upcoming_events,
        zoo=zoo,  # type: ignore
        daily_checkout_count=daily_event_count,
        daily_checkout_duration=daily_event_duration,
        weekly_event_activity_hours=weekly_event_activity.total_seconds() / 3600,
    )


@router.get("/details/resting")
async def get_resting_animals(session: AsyncSession = Depends(get_db_session)) -> list[RestingAnimal]:
    animals_status = await get_animals_status(session)

    resting_animals = list(
        filter(
            lambda animal: "resting" in animal.status_description.lower(),
            animals_status,
        )
    )

    # weekly event activity
    events = await session.exec(
        select(AnimalEvent).where(col(AnimalEvent.checked_in).isnot(None))
    )
    events = list(events.all())

    weekly_event_activity = sum(
        (event.duration for event in events if event.duration), timedelta(0)
    )
    weekly_event_activity_hours = weekly_event_activity.total_seconds() / 3600

    return [
        RestingAnimal(
            animal_status=animal,
            weekly_event_activity_hours=weekly_event_activity_hours,
            daily_checkout_count=animal.daily_event_count,
            daily_checkout_duration=animal.daily_event_duration,
            health_logs=await get_animal_health_logs(animal.animal.id, session),
        )
        for animal in resting_animals
    ]


@router.get("/details/checkedout")
async def get_checked_out_animals(session: AsyncSession = Depends(get_db_session)) -> list[AnimalWithCurrentEvent]:
    animals = await session.exec(
        select(Animal, AnimalEvent)
        .join(AnimalEvent)
        .where(
            and_(
                col(AnimalEvent.checked_out).isnot(None),
                col(AnimalEvent.checked_in).is_(None),
            )
        )
    )
    animals = list(animals.all())

    events_ids = [animal_event.event_id for animal, animal_event in animals]
    events = await session.exec(select(Event).where(col(Event.id).in_(events_ids)))
    events = list(events.unique())

    events_details = await get_events_details(session, events)

    animals_with_events = []
    for animal, animal_event in animals:
        event = next(
            (
                event
                for event in events_details
                if event.event.id == animal_event.event_id
            ),
            None,
        )
        animals_with_events.append(
            AnimalWithCurrentEvent(
                animal=animal,
                current_event=event,  # type: ignore
            )
        )

    return animals_with_events


@router.post("/")
async def create_animal(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    name: str = Form(...),
    species: str = Form(...),
    max_daily_checkouts: str = Form(...),
    max_daily_checkout_hours: str = Form(""),
    rest_time: str = Form(""),
    handling_enabled: str = Form(...),
    zoo_id: str = Form(...),
    description: str = Form(""),
    tier: str = Form("1"),
    image: UploadFile = File(None),
):
    # Check permissions first
    if not has_permission(current_user.role.permissions, "add_animal"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Validate and parse required fields
    if not name or name.strip() == "":
        raise HTTPException(status_code=422, detail="Name is required")
    if not species or species.strip() == "":
        raise HTTPException(status_code=422, detail="Species is required")
        
    # Parse required integer fields
    parsed_max_daily_checkouts = parse_form_int(max_daily_checkouts)
    if parsed_max_daily_checkouts is None or parsed_max_daily_checkouts <= 0:
        raise HTTPException(status_code=422, detail="Max daily checkouts must be a positive integer")
    
    parsed_zoo_id = parse_form_int(zoo_id)
    if parsed_zoo_id is None:
        raise HTTPException(status_code=422, detail="Zoo ID must be a valid integer")
    
    # Parse boolean field
    parsed_handling_enabled = parse_form_boolean(handling_enabled)
    
    # Parse optional fields
    parsed_max_daily_checkout_hours = parse_form_int(max_daily_checkout_hours)
    parsed_rest_time = parse_form_float(rest_time)
    parsed_tier = parse_form_int(tier) or 1  # Default to 1 if not provided

    # Handle image upload
    image_filename_to_save = None
    if image and image.filename and image.size > 0:
        if not image.content_type or not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")
        
        # Ensure image directory exists
        IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        extension = Path(image.filename).suffix if image.filename else ".jpg"
        unique_filename = f"{uuid.uuid4()}{extension}"
        file_location = IMAGE_DIR / unique_filename

        # Save the file
        try:
            with file_location.open("wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            image_filename_to_save = unique_filename
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error saving image file.")
        finally:
            image.file.close()

    # Create the animal
    try:
        # Get user ID before any async operations to avoid greenlet issues
        user_id = current_user.id
        
        animal_data = AnimalIn(
            name=name.strip(),
            species=species.strip(),
            max_daily_checkouts=parsed_max_daily_checkouts,
            max_daily_checkout_hours=parsed_max_daily_checkout_hours,
            rest_time=parsed_rest_time,
            handling_enabled=parsed_handling_enabled,
            zoo_id=parsed_zoo_id,
            description=description.strip() if description else None,
            tier=parsed_tier,
            image_filename=image_filename_to_save,
            daily_checkout_count=0,
            daily_checkout_duration=timedelta(hours=0),
            last_checkin_time=None,
            checked_in=True,
            status="checked_in"
        )
        
        # Create Animal object directly from the AnimalIn data
        db_animal = Animal(**animal_data.model_dump())
        
        session.add(db_animal)
        await session.commit()
        await session.refresh(db_animal)

        # Log audit with the user_id we captured earlier
        try:
            await log_audit(
                session=session,
                animal_id=db_animal.id,
                changed_by=user_id,
                action="created",
            )
        except Exception as audit_error:
            # Don't fail the whole operation if audit logging fails
            pass

        return db_animal
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.delete("/{animal_id}")
async def delete_animal(animal_id: int, session: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    if not has_permission(current_user.role.permissions, "delete_animals"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    animal = await get_animal_by_id(animal_id, session)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    # log audit
    await log_audit(
        session,
        animal_id=animal.id,
        changed_by=current_user.id,
        action="animal_deleted",
        description=f"{current_user.first_name} {current_user.last_name} ({current_user.role.name}) deleted an animal with name {animal.name}",
    )

    # delete animal events records
    animal_events = await session.exec(
        select(AnimalEvent).where(col(AnimalEvent.animal_id) == animal_id)
    )
    for animal_event in animal_events.unique():
        await session.delete(animal_event)

    # delete animal audits
    audits = await session.exec(
        select(AnimalAudit).where(col(AnimalAudit.animal_id) == animal_id)
    )
    for audit in audits.unique():
        await session.delete(audit)

    # delete animal health logs
    logs = await session.exec(
        select(AnimalHealthLog).where(col(AnimalHealthLog.animal_id) == animal_id)
    )
    for log in logs.unique():
        await session.delete(log)

    await session.refresh(animal)
    await session.delete(animal)
    await session.commit()

    return {"message": "Animal deleted"}


@router.put("/{animal_id}")
async def update_animal(
    animal_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    name: str = Form(...),
    species: str = Form(...),
    max_daily_checkouts: int = Form(...),
    max_daily_checkout_hours: int | None = Form(None),
    rest_time: float | None = Form(None),  # Changed to optional to match create_animal
    handling_enabled: bool = Form(...),
    zoo_id: int = Form(...),
    description: str | None = Form(None),
    tier: int = Form(1),
    checked_in: bool = Form(...), # Keep checked_in status if provided
    status: str | None = Form(None), # Keep status if provided
    image: UploadFile | None = File(None), # Changed from animal_update: AnimalIn
):
    if not has_permission(current_user.role.permissions, "update_animal"):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_animal = await get_animal_by_id(animal_id, session)
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    # Ensure image directory exists
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    update_data = {
        "name": name,
        "species": species,
        "max_daily_checkouts": max_daily_checkouts,
        "max_daily_checkout_hours": max_daily_checkout_hours,
        "rest_time": rest_time,
        "handling_enabled": handling_enabled,
        "zoo_id": zoo_id,
        "description": description,
        "tier": tier,
        "checked_in": checked_in,
        "status": status if status is not None else db_animal.status # Keep old status if not provided
    }
    image_filename_to_save = db_animal.image_filename # Keep old image by default

    if image:
        if not image.content_type or not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400, detail="Invalid file type. Only images are allowed."
            )
        # Generate unique filename
        extension = Path(image.filename).suffix if image.filename else ".jpg"
        unique_filename = f"{uuid.uuid4()}{extension}"
        file_location = IMAGE_DIR / unique_filename

        # Delete old image file if it exists
        if db_animal.image_filename:
            old_file_path = IMAGE_DIR / db_animal.image_filename
            if old_file_path.is_file():
                old_file_path.unlink()

        # Save the new file
        try:
            with file_location.open("wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            image_filename_to_save = unique_filename
        except Exception as e:
            print(f"Error saving file: {e}")
            raise HTTPException(status_code=500, detail="Error saving image file.")
        finally:
            image.file.close()

    update_data["image_filename"] = image_filename_to_save

    # Log changes before updating
    changed_fields = await log_fields_update(
        session=session,
        user_id=current_user.id,
        animal_id=db_animal.id,
        old_data=db_animal,
        new_data=update_data,
    )

    # Update the animal object
    for key, value in update_data.items():
        setattr(db_animal, key, value)

    session.add(db_animal)
    await session.commit()
    await session.refresh(db_animal)

    if changed_fields:
      await log_audit(
          session=session,
          animal_id=db_animal.id,
          changed_by=current_user.id,
          action="updated",
          description=f"Fields updated: {', '.join(changed_fields)}"
      )

    return db_animal


@router.put("/{animal_id}/unavailable")
async def mark_animal_unavailable(
    animal_id: int, session: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)
):
    if not has_permission(current_user.role.permissions, "make_animal_unavailable"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    await toggle_animal_availability(session, animal_id, current_user.id, "unavailable")
    return JSONResponse(
        content={"message": "Animal marked unavailable"}, status_code=200
    )


@router.put("/{animal_id}/available")
async def mark_animal_available(
    animal_id: int, session: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)
):
    if not has_permission(current_user.role.permissions, "make_animal_available"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    await toggle_animal_availability(session, animal_id, current_user.id, "available")
    return JSONResponse(content={"message": "Animal marked available"}, status_code=200)


@router.get("/{animal_id}/audits")
async def get_animal_audits(
    animal_id: int, session: AsyncSession = Depends(get_db_session)
) -> list[AnimalAuditWithDetails]:
    animal = await get_animal_by_id(animal_id, session)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    audits = await session.exec(
        select(AnimalAudit)
        .where(col(AnimalAudit.animal_id) == animal_id)
        .order_by(desc(AnimalAudit.changed_at))
    )
    audits = audits.unique()

    return [
        AnimalAuditWithDetails(audit=audit, animal=audit.animal, user=audit.user)
        for audit in audits
    ]


@router.get("/{animal_id}/health-log")
async def get_animal_health_logs(
    animal_id: int, session: AsyncSession = Depends(get_db_session)
) -> list[AnimalHealthLogWithDetails]:
    return await retrieve_animal_logs(animal_id, session)


@router.post("/{animal_id}/health-log")
async def create_animal_health_log(
    animal_id: int,
    body: AnimalHealthLogIn,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    if not has_permission(current_user.role.permissions, "add_animal_health_log"):
        raise HTTPException(
            status_code=401, detail="Not Authorized to perform this action"
        )

    animal = await get_animal_by_id(animal_id, session)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    log = AnimalHealthLog(
        details=body.details, logged_by=current_user.id, animal_id=animal_id
    )  # type: ignore
    session.add(log)
    await session.commit()
    await session.refresh(animal)
    await session.refresh(log)

    await log_audit(
        session,
        animal_id=animal.id,
        changed_by=current_user.id,
        action="health_log_added",
        description=f"{current_user.first_name} {current_user.last_name} ({current_user.role.name}) created a health log",
        changed_field="health_log",
        old_value=None,
        new_value=log.details,
    )

    return JSONResponse(content={"message": "Health log created"}, status_code=200)


@router.put("/{animal_id}/health-log/{log_id}")
async def update_animal_health_log(
    animal_id: int,
    log_id: int,
    body: AnimalHealthLogIn,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    if not has_permission(current_user.role.permissions, "add_animal_health_log"):
        raise HTTPException(
            status_code=401, detail="Not Authorized to perform this action"
        )

    animal = await get_animal_by_id(animal_id, session)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    log = (
        await session.exec(
            select(AnimalHealthLog).where(col(AnimalHealthLog.id) == log_id)
        )
    ).first()
    if not log:
        raise HTTPException(status_code=404, detail="Health log not found")

    if log.logged_by != current_user.id:
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    old_log = str(log.details)

    log.details = body.details
    await session.commit()
    await session.refresh(animal)
    await session.refresh(log)

    await log_audit(
        session,
        animal_id=animal.id,
        changed_by=current_user.id,
        action="health_log_updated",
        description=f"{current_user.first_name} {current_user.last_name} ({current_user.role.name}) updated a health log",
        changed_field="health_log",
        old_value=old_log,
        new_value=body.details,
    )

    return JSONResponse(content={"message": "Health log updated"}, status_code=200)

from datetime import UTC, datetime

from models import Animal, AnimalActitvityLog, AnimalAudit, AnimalEvent
from sqlmodel import and_, col, select


async def get_all_animals(zoo_id: int | None, session) -> list[Animal]:
    if zoo_id:
        animals = await session.exec(select(Animal).where(Animal.zoo_id == zoo_id))
    else:
        animals = await session.exec(select(Animal))

    return animals.all()


async def get_animal_by_id(id: int, session) -> Animal | None:
    animal = (await session.exec(select(Animal).where(Animal.id == id))).first()
    return animal


async def update_animals_status(session):
    animals = await get_all_animals(None, session)
    current_time = datetime.now(UTC)

    for animal in animals:
        # get all ongoing events for the animal
        event_links = await session.exec(
            select(AnimalEvent).where(
                and_(
                    AnimalEvent.animal_id == animal.id,
                    col(AnimalEvent.checked_out) <= current_time,
                    col(AnimalEvent.checked_in) >= current_time,
                )
            )
        )

        if event_links.all():
            ...


async def log_activity(animal_id: int, details: str, session):
    log = AnimalActitvityLog(animal_id=animal_id, details=details)
    session.add(log)
    await session.commit()
    return log


async def log_audit(
    animal_id: int,
    changed_by: int,
    changed_field: str,
    old_value: str,
    new_value: str,
    session,
):
    log = AnimalAudit(
        animal_id=animal_id,
        changed_by=changed_by,
        changed_field=changed_field,
        old_value=old_value,
        new_value=new_value,
    )
    session.add(log)
    await session.commit()
    return log

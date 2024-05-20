from sqlmodel import select

from models import Event


async def get_all_events(session, zoo_id: int | None = None) -> list[Event]:
    if zoo_id:
        events = await session.exec(select(Event).where(Event.zoo_id == zoo_id))
    else:
        events = await session.exec(select(Event))

    return events.all()


async def get_event_by_id(id: int, session) -> Event | None:
    event = (await session.exec(select(Event).where(Event.id == id))).first()
    return event
from core.config import settings
from models import Zoo
from sqlmodel import select


async def get_zoo(session) -> list[Zoo] | None:
    zoos = await session.exec(select(Zoo))
    return zoos.all()


async def get_zoo_by_id(id: int, session) -> Zoo | None:
    zoo = (await session.exec(select(Zoo).where(Zoo.id == id))).first()
    return zoo


async def get_zoo_by_name(name: str, session) -> Zoo | None:
    zoo = (await session.exec(select(Zoo).where(Zoo.name == name))).first()
    return zoo


async def get_main_zoo(session) -> Zoo | None:
    zoo = (await session.exec(select(Zoo).where(Zoo.name == settings.ZOO_NAME))).first()
    return zoo

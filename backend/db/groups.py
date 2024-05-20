from models import Group
from sqlmodel import select


async def get_groups(session) -> list[Group] | None:
    groups = await session.exec(select(Group))
    return groups.all()


async def get_group_by_id(id: int, session) -> Group | None:
    group = (await session.exec(select(Group).where(Group.id == id))).first()
    return group

from models import Animal
from sqlmodel import select


async def get_all_animals(zoo_id: int | None, session) -> list[Animal]:
    if zoo_id:
        animals = await session.exec(select(Animal).where(Animal.zoo_id == zoo_id))
    else:
        animals = await session.exec(select(Animal))

    return animals.all()


async def get_animal_by_id(id: int, session) -> Animal | None:
    animal = (await session.exec(select(Animal).where(Animal.id == id))).first()
    return animal

from api.deps import CurrentUser, SessionDep
from db.animals import get_all_animals, get_animal_by_id
from db.utils import has_permission
from fastapi import APIRouter, HTTPException
from models import Animal, AnimalIn, Event

router = APIRouter(prefix="/animals", tags=["Animals"])


@router.get("/")
async def read_all_animals(
    session: SessionDep, zoo_id: int | None = None
) -> list[Animal]:
    return await get_all_animals(zoo_id, session)


@router.post("/")
async def create_animal(
    animal: Animal, session: SessionDep, current_user: CurrentUser
) -> Animal:
    print(current_user.role.permissions)

    if not has_permission(current_user.role.permissions, "manage_animals"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    session.add(animal)
    await session.commit()
    await session.refresh(animal)
    return animal


@router.put("/{animal_id}")
async def update_animal(
    animal_id: int,
    animal_update: AnimalIn,
    session: SessionDep,
    current_user: CurrentUser,
) -> Animal:
    if not has_permission(current_user.role.permissions, "manage_animals"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    animal = await get_animal_by_id(animal_id, session)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    for field, value in animal_update.model_dump().items():
        setattr(animal, field, value)

    await session.commit()
    await session.refresh(animal)
    return animal

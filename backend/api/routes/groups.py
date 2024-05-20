from api.deps import CurrentUser, SessionDep
from db.groups import get_group_by_id, get_groups
from db.users import get_user_by_id
from db.utils import has_permission
from fastapi import APIRouter, Body, HTTPException
from models import (
    Group,
    GroupIn,
    GroupWithMembers,
    GroupWithZoo,
    MemberShip,
    User,
)
from sqlmodel import select

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("/", response_model=list[GroupWithZoo])
async def read_all_groups(
    session: SessionDep, current_user: CurrentUser
) -> list[GroupWithZoo]:
    if not has_permission(current_user.role.permissions, "manage_users"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    return await get_groups(session)


@router.post("/")
async def create_group(
    session: SessionDep, current_user: CurrentUser, group: GroupIn = Body(...)
):
    if not has_permission(current_user.role.permissions, "manage_users"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    new_group = Group(title=group.title, zoo_id=group.zoo_id)
    session.add(new_group)
    await session.commit()

    return {"message": "Group created successfully"}


@router.get("/{group_id}", response_model=GroupWithZoo)
async def read_group_by_id(
    group_id: int, session: SessionDep, current_user: CurrentUser
) -> GroupWithZoo:
    if not has_permission(current_user.role.permissions, "manage_users"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    group = await get_group_by_id(group_id, session)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.post("/{group_id}/add-member/{user_id}")
async def add_member_to_group(
    group_id: int, user_id: int, session: SessionDep, current_user: CurrentUser
):
    if not has_permission(current_user.role.permissions, "manage_users"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    group = await get_group_by_id(group_id, session)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    user = await get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    membership = (
        await session.exec(
            select(MemberShip).where(
                MemberShip.user_id == user_id, MemberShip.group_id == group_id
            )
        )
    ).first()
    if membership:
        raise HTTPException(
            status_code=400, detail="User is already a member of this group"
        )

    membership = MemberShip(user_id=user_id, group_id=group_id)
    session.add(membership)
    await session.commit()

    return {"message": "User added to group successfully"}


@router.post("/{group_id}/remove-member/{user_id}")
async def remove_member_from_group(
    group_id: int, user_id: int, session: SessionDep, current_user: CurrentUser
):
    if not has_permission(current_user.role.permissions, "manage_users"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    group = await get_group_by_id(group_id, session)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    user = await get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    membership = (
        await session.exec(
            select(MemberShip).where(
                MemberShip.user_id == user_id, MemberShip.group_id == group_id
            )
        )
    ).first()
    if not membership:
        raise HTTPException(
            status_code=400, detail="User is not a member of this group"
        )

    session.delete(membership)
    await session.commit()

    return {"message": "User removed from group successfully"}


@router.get("/{group_id}/members", response_model=GroupWithMembers)
async def get_group_members(
    group_id: int, session: SessionDep, current_user: CurrentUser
):
    if not has_permission(current_user.role.permissions, "manage_users"):
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )

    group = await get_group_by_id(group_id, session)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    member_users = await session.exec(
        select(User).join(MemberShip).where(MemberShip.group_id == group_id)
    )

    return GroupWithMembers(group=group, members=member_users.all())

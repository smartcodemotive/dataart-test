from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import User
from app.schemas import UserCreate, UserListResponse, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserResponse,
    summary="Create a user",
    description="Create a new user. Email must be unique.",
)
async def create_user(user_in: UserCreate, session: AsyncSession = Depends(get_session)) -> User:
    result = await session.execute(select(User).where(User.email == user_in.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=user_in.email, name=user_in.name)
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a single user by ID.",
)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)) -> User:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get(
    "",
    response_model=UserListResponse,
    summary="List users",
    description="List users with pagination (limit and offset).",
)
async def list_users(
    session: AsyncSession = Depends(get_session),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> UserListResponse:
    count_result = await session.execute(select(func.count()).select_from(User))
    total = count_result.scalar() or 0
    result = await session.execute(select(User).limit(limit).offset(offset))
    users = result.scalars().all()
    return UserListResponse(
        items=[UserResponse.model_validate(u) for u in users],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Delete user",
    description="Delete a user by ID. Associated projects are updated (owner reference removed or cascade).",
)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)) -> None:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.flush()

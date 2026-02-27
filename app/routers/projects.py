from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Project, User
from app.schemas import ProjectCreate, ProjectResponse

router = APIRouter(tags=["Projects"])


@router.post(
    "/projects",
    response_model=ProjectResponse,
    summary="Create a project",
    description="Create a project for an existing user (owner_id must exist).",
)
async def create_project(
    project_in: ProjectCreate, session: AsyncSession = Depends(get_session)
) -> Project:
    result = await session.execute(select(User).where(User.id == project_in.owner_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User not found")
    project = Project(
        name=project_in.name,
        description=project_in.description,
        owner_id=project_in.owner_id,
    )
    session.add(project)
    await session.flush()
    await session.refresh(project)
    return project


@router.get(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    summary="Get project by ID",
    description="Retrieve a single project by ID.",
)
async def get_project(
    project_id: int, session: AsyncSession = Depends(get_session)
) -> Project:
    result = await session.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get(
    "/users/{user_id}/projects",
    response_model=list[ProjectResponse],
    summary="List user's projects",
    description="List all projects owned by the given user.",
)
async def list_user_projects(
    user_id: int, session: AsyncSession = Depends(get_session)
) -> list[Project]:
    result = await session.execute(select(User).where(User.id == user_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")
    result = await session.execute(select(Project).where(Project.owner_id == user_id))
    projects = result.scalars().all()
    return list(projects)

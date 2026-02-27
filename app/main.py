from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_schema
from app.routers import projects, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_schema()
    yield


app = FastAPI(
    title="Mini User & Project Management API",
    description="REST API for managing users and their projects.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router)
app.include_router(projects.router)


@app.get("/health")
async def health():
    return {"status": "ok"}

# Mini User & Project Management API

A small REST API built with **FastAPI**, **Pydantic**, and **SQLModel** (async SQLAlchemy). It manages **Users** and **Projects** with a one-to-many relationship (one user, many projects).

## Run with Docker (no manual steps)

From the project root:

```bash
docker-compose up
```

- API: **http://localhost:8000**
- Docs: **http://localhost:8000/docs**
- Database schema is created automatically on startup.

## Run locally (without Docker)

Uses **SQLite** by default (no PostgreSQL needed):

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: **http://localhost:8000**
- Data is stored in `local.db` in the project root.

To use PostgreSQL instead, set `DATABASE_URL` (e.g. `postgresql+asyncpg://user:password@localhost:5432/appdb`).

## API Endpoints

### Users
- `POST /users` — Create user (email must be unique)
- `GET /users/{id}` — Get user by ID
- `GET /users` — List users (query: `limit`, `offset`)
- `DELETE /users/{id}` — Delete user (projects are cascade-deleted)

### Projects
- `POST /projects` — Create project for an existing user (`owner_id` required)
- `GET /projects/{id}` — Get project by ID
- `GET /users/{id}/projects` — List all projects for a user

## Tech stack

- **FastAPI** — API framework
- **Pydantic** — Request/response validation
- **SQLModel** — ORM (SQLAlchemy + Pydantic)
- **PostgreSQL** — Database (via Docker)
- **Async** — Async engine and sessions, dependency-injected DB session

## Tests

With a local Python env and dependencies installed:

```bash
pip install -r requirements.txt
pytest
```

Tests use an in-memory SQLite DB and override the session dependency; no Docker required.

## Project layout

```
app/
  main.py       # FastAPI app, lifespan, schema creation
  config.py     # Settings (e.g. DATABASE_URL)
  database.py   # Async engine, session factory, get_session
  models.py     # User, Project (SQLModel)
  schemas.py    # Pydantic request/response models
  routers/
    users.py    # User CRUD + list
    projects.py # Project CRUD + list by user
tests/
  conftest.py   # Async client, test DB, overrides
  test_api.py   # API tests
docker-compose.yml
Dockerfile
requirements.txt
```

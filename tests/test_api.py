import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_and_get_user(client: AsyncClient):
    r = await client.post("/users", json={"email": "alice@example.com", "name": "Alice"})
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "alice@example.com"
    assert data["name"] == "Alice"
    assert "id" in data
    user_id = data["id"]

    r2 = await client.get(f"/users/{user_id}")
    assert r2.status_code == 200
    assert r2.json()["email"] == "alice@example.com"


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient):
    await client.post("/users", json={"email": "bob@example.com", "name": "Bob"})
    r = await client.post("/users", json={"email": "bob@example.com", "name": "Bob Again"})
    assert r.status_code == 400
    assert "already registered" in r.json()["detail"].lower() or "unique" in r.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient):
    r = await client.get("/users/99999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_list_users_pagination(client: AsyncClient):
    for i in range(3):
        await client.post("/users", json={"email": f"u{i}@example.com", "name": f"User {i}"})
    r = await client.get("/users?limit=2&offset=0")
    assert r.status_code == 200
    data = r.json()
    assert len(data["items"]) == 2
    assert data["total"] == 3
    assert data["limit"] == 2
    assert data["offset"] == 0

    r2 = await client.get("/users?limit=2&offset=2")
    assert r2.status_code == 200
    assert len(r2.json()["items"]) == 1


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    r = await client.post("/users", json={"email": "del@example.com", "name": "Delete Me"})
    user_id = r.json()["id"]
    r = await client.delete(f"/users/{user_id}")
    assert r.status_code == 204
    r = await client.get(f"/users/{user_id}")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_create_project_for_user(client: AsyncClient):
    r = await client.post("/users", json={"email": "owner@example.com", "name": "Owner"})
    owner_id = r.json()["id"]
    r = await client.post(
        "/projects",
        json={"name": "My Project", "description": "A project", "owner_id": owner_id},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "My Project"
    assert data["owner_id"] == owner_id
    assert "id" in data

    r2 = await client.get(f"/projects/{data['id']}")
    assert r2.status_code == 200
    assert r2.json()["name"] == "My Project"


@pytest.mark.asyncio
async def test_create_project_user_not_found(client: AsyncClient):
    r = await client.post(
        "/projects",
        json={"name": "Orphan", "description": "", "owner_id": 99999},
    )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_list_user_projects(client: AsyncClient):
    r = await client.post("/users", json={"email": "powner@example.com", "name": "Project Owner"})
    owner_id = r.json()["id"]
    await client.post(
        "/projects",
        json={"name": "P1", "description": "", "owner_id": owner_id},
    )
    await client.post(
        "/projects",
        json={"name": "P2", "description": "", "owner_id": owner_id},
    )
    r = await client.get(f"/users/{owner_id}/projects")
    assert r.status_code == 200
    projects = r.json()
    assert len(projects) == 2
    names = {p["name"] for p in projects}
    assert names == {"P1", "P2"}


@pytest.mark.asyncio
async def test_delete_user_cascades_projects(client: AsyncClient):
    r = await client.post("/users", json={"email": "cascade@example.com", "name": "Cascade"})
    owner_id = r.json()["id"]
    r = await client.post(
        "/projects",
        json={"name": "To Delete", "description": "", "owner_id": owner_id},
    )
    project_id = r.json()["id"]
    await client.delete(f"/users/{owner_id}")
    r = await client.get(f"/projects/{project_id}")
    assert r.status_code == 404

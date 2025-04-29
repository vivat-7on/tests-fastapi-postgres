import httpx
import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport

from app.database import get_connection
from app.main import app


@pytest.fixture
async def async_client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport,
                                     base_url="http://testserver") as client:
            yield client


@pytest.fixture(autouse=True)
async def cleaning_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users")
    connection.commit()
    connection.close()


class TestUserApi:

    @pytest.mark.asyncio
    async def test_say_hello_async(self, async_client):
        response = await async_client.get("/hello")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World!"}

    @pytest.mark.asyncio
    async def test_create_user_async(self, async_client):
        response = await async_client.post("/users", json={"name": "Valera"})
        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "created"
        assert data["name"] == "Valera"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_get_user_async(self, async_client):
        response = await async_client.post("/users", json={"name": "Valera"})
        assert response.status_code == 200
        user_id = response.json()["id"]

        response = await async_client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Valera"
        assert response.json()["id"] == user_id

    @pytest.mark.asyncio
    async def test_delete_user_async(self, async_client):
        response = await async_client.post("/users", json={"name": "Valera"})
        assert response.status_code == 200
        user_id = response.json()["id"]

        response = await async_client.delete(f"/users/{user_id}")
        assert response.status_code == 200

        response = await async_client.get(f"/users/{user_id}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "name, expected_status",
        [
            ("Valera", 200),
            ("TestUser", 200),
            ("", 422),
        ]
    )
    async def test_create_user_parametrize(self, async_client, name,
                                           expected_status):
        response = await async_client.post("/users", json={"name": name})
        assert response.status_code == expected_status
        if expected_status == 200:
            data = response.json()
            assert data["status"] == "created"
            assert data["name"] == name
            assert "id" in data

    @pytest.mark.asyncio
    async def test_delete_non_existing_user(self, async_client):
        response = await async_client.delete("/users/999999")
        assert response.status_code == 404

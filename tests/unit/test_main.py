import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.unit
def test_say_hello():
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}


@pytest.mark.unit
def test_slow_response():
    response = client.get("/slow")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "response": "That was slow..."}


class TestMainApi:
    @pytest.mark.parametrize(
        "name, expect_status",
        [
            ("Valera", 200),
            ("TestUser", 200),
            ("", 422),
        ]
    )
    def test_create_user(self, client, name, expect_status):
        response = client.post('/users', json={"name": name})
        assert response.status_code == expect_status
        data = response.json()
        if response.status_code == 200:
            assert data["name"] == name
            assert data["status"] == "created"

    @pytest.mark.integration
    def test_delete_user(self, client):
        response = client.post("/users", json={"name": "Valera"})
        assert response.status_code == 200

        response = client.get("/users")
        assert response.status_code == 200
        users = response.json()
        user_id = users[-1]["id"]

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json() == {"status": "deleted", "id": user_id}

        response = client.get(f"/users/{user_id}")
        assert response.status_code == 404

    @pytest.mark.integration
    def test_get_user(self, client):
        response = client.post("/users", json={"name": "Valera"})
        assert response.status_code == 200

        response = client.get("/users")
        assert response.status_code == 200
        users = response.json()
        user_id = users[-1]["id"]

        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["id"] == user_id
        assert response.json()["name"] == "Valera"

    @pytest.mark.parametrize(
        "id, expected_status",
        [
            (9999, 404),
            (12345, 404),
            (0, 404),
        ]
    )
    def test_delete_non_existing_users(self, client, id, expected_status):
        response = client.delete(f"/users/{id}")
        assert response.status_code == expected_status

    @pytest.mark.integration
    def test_create_delete_get_user(self, client):
        response = client.post("/users", json={"name": "Valera"})
        assert response.status_code == 200

        response = client.get("/users")
        user = response.json()[-1]
        user_id = user["id"]
        assert user["name"] == "Valera"

        response = client.get(f"/users/{user_id}")
        assert response.json()["name"] == "Valera"

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200

        response = client.get(f"/users/{user_id}")
        assert response.status_code == 404

    @pytest.mark.integration
    def test_double_deleting_user(self, client):
        response = client.post("/users", json={"name": "Valera"})
        assert response.status_code == 200

        response = client.get("/users")
        user = response.json()[-1]
        user_id = user["id"]
        assert user["name"] == "Valera"

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 404

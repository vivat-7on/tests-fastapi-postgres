import pytest
from starlette.testclient import TestClient

from app.database import get_connection, setup_db
from app.main import app, get_db


@pytest.fixture
def conn():
    connection = get_connection()
    setup_db(connection)
    yield connection
    connection.close()


@pytest.fixture
def client(conn):
    app.dependency_overrides[get_db] = lambda: conn
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}
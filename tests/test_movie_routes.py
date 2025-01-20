from fastapi.testclient import TestClient
from ex6.main import app
from ex6.tests.init_test_db import engine

client = TestClient(app)


def test_read_movies():
    response = client.get("/movies")
    assert response.status_code == 200

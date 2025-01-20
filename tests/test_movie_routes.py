import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from ex6.main import app
from ex6.routes.movie_routes import get_session
from ex6.models.movie_models import MovieOut


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        try:
            session.begin()
            yield session
        finally:
            session.rollback()
            session.close()


@pytest.fixture(name="db_init")
def db_init_fixture(session: Session):
    initial_data = [
        MovieOut(
            title="Amazing Movie", director="Anne Bee", category="action", year=1996
        ),
        MovieOut(
            title="Fantastic Film", director="Cee Dee", category="sci-fi", year=2013
        ),
        MovieOut(
            title="Epic Adventure", director="John Doe", category="adventure", year=2005
        ),
    ]

    for movie in initial_data:
        session.add(movie)

    session.commit()


@pytest.fixture(name="client")
def client_fixture(session: Session, db_init):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


def test_get_all_movies(client: TestClient):
    response = client.get("/movies")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


def test_get_movie_by_id_when_existing(client: TestClient):
    response = client.get("/movies/1")
    assert response.status_code == 200
    assert response.json() == {
        "title": "Amazing Movie",
        "director": "Anne Bee",
        "category": "action",
        "year": 1996,
        "id": 1,
    }


def test_get_movie_by_id_when_nonexistent(client: TestClient):
    response = client.get("/movies/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie not found"}


def test_add_movie_when_data_ok(client: TestClient):
    response = client.post(
        "/movies",
        json={
            "title": "Test Title",
            "director": "Test Director",
            "category": "test category",
            "year": 2000,
        },
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Movie added successfully"}


def test_add_movie_when_title_empty(client: TestClient):
    response = client.post(
        "/movies",
        json={
            "title": "",
            "director": "Test Director",
            "category": "test category",
            "year": 2000,
        },
    )

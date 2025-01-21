import pytest
from pydantic import ValidationError
from ex6.models.movie_models import MovieBase, MovieOut, MovieIn


def test_movie_base_valid():
    movie = MovieBase(
        title="Test Movie",
        director="Test Director",
        category="test category",
        year=2010,
    )

    assert movie.title == "Test Movie"
    assert movie.director == "Test Director"
    assert movie.category == "test category"
    assert movie.year == 2010


def test_movie_base_empty_title():
    with pytest.raises(ValidationError) as err:
        movie = MovieBase(
            title="",
            director="Test Director",
            category="test category",
            year=2010,
        )

    assert "String should have at least 1 character" in str(err.value)

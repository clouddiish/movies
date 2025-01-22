import pytest
from pydantic import ValidationError
from movies.models.movie_models import MovieBase, MovieOut, MovieIn


def test_movie_base_valid():
    """Test that MovieBase accepts valid input data.

    Ensures that all fields in the MovieBase model are properly assigned
    when provided with valid input data.
    """
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
    """Test that MovieBase raises a ValidationError for an empty title.

    Verifies that the title field in the MovieBase model cannot be empty,
    and raises the appropriate ValidationError.
    """
    with pytest.raises(ValidationError) as err:
        movie = MovieBase(
            title="",
            director="Test Director",
            category="test category",
            year=2010,
        )

    assert "String should have at least 1 character" in str(err.value)


def test_movie_out_inherits_movie_base():
    """Test that MovieOut inherits from MovieBase and includes an id field.

    Verifies that the MovieOut model extends MovieBase by adding the
    `id` field, and that all fields are correctly assigned when provided
    with valid input data.
    """
    movie = MovieOut(
        id=1,
        title="Test Movie",
        director="Test Director",
        category="test category",
        year=2010,
    )

    assert movie.id == 1
    assert movie.title == "Test Movie"
    assert movie.director == "Test Director"
    assert movie.category == "test category"
    assert movie.year == 2010


def test_movie_in_excludes_id():
    """Test that MovieIn excludes the id field.

    Verifies that the MovieIn model, which is intended for input data,
    does not include the `id` field and accepts other valid fields.
    """
    movie = MovieIn(
        title="Test Movie",
        director="Test Director",
        category="test category",
        year=2010,
    )

    assert not hasattr(movie, "id")
    assert movie.title == "Test Movie"
    assert movie.director == "Test Director"
    assert movie.category == "test category"
    assert movie.year == 2010

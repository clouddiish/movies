from sqlmodel import SQLModel, Field


class MovieBase(SQLModel):
    """Base model for movie data.

    Attributes:
        title (str): Title of the movie.
        director (str): Director of the movie.
        category (str): Genre or category of the movie.
        year (int): Year the movie was released.
    """

    title: str = Field(min_length=1)
    director: str = Field(min_length=1)
    category: str = Field(min_length=1)
    year: int = Field(gt=0)


class MovieOut(MovieBase, table=True):
    """Model for movie data with an ID attribute.

    Attributes:
        id (int): Unique identifier of the movie.
    """

    id: int | None = Field(default=None, primary_key=True)


class MovieIn(MovieBase):
    """Model for incoming movie data (without ID)."""

    pass

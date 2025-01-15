from sqlmodel import SQLModel, Field


class MovieBase(SQLModel):
    """Base model for movie data.

    Attributes:
        title (str): Title of the movie.
        director (str): Director of the movie.
        category (str): Genre or category of the movie.
        year (int): Year the movie was released.
    """

    title: str = Field(min_length=1, description="The title cannot be empty")
    director: str = Field(min_length=1, description="The director cannot be empty")
    category: str = Field(min_length=1, description="The category cannot be empty")
    year: int = Field(gt=0, description="The year must be a positive integer")


class MovieOut(MovieBase, table=True):
    """Model for movie data with an ID attribute.

    Attributes:
        id (int): Unique identifier of the movie.
    """

    id: int | None = Field(default=None, primary_key=True)


class MovieIn(MovieBase):
    """Model for incoming movie data (without ID)."""

    pass

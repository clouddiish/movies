import sqlite3
from typing import Annotated
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

TABLE_HEADERS = ["id", "title", "director", "category", "year"]
DATABASE = "movies.db"


class MovieBase(BaseModel):
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


class MovieOut(MovieBase):
    """Model for movie data with an ID attribute.

    Attributes:
        id (int): Unique identifier of the movie.
    """

    id: int


class MovieIn(MovieBase):
    """Model for incoming movie data (without ID)."""

    pass


def convert_results(results):
    """Converts database query results to a list of dictionaries.

    Args:
        results (list): List of tuples from database query.

    Returns:
        list: List of dictionaries representing movies.
    """
    results_arr = []

    for row in results:
        inner_dict = {}
        i = 0
        for header in TABLE_HEADERS:
            inner_dict[header] = row[i]
            i += 1
        results_arr.append(inner_dict)

    return results_arr


def convert_result(result):
    """Converts a single database query result to a dictionary.

    Args:
        result (tuple): Single tuple from database query.

    Returns:
        dict: Dictionary representing a movie.
    """
    result_dict = {}
    i = 0

    for header in TABLE_HEADERS:
        result_dict[header] = result[i]
        i += 1

    return result_dict


def does_movie_with_id_exist(id):
    """Checks if a movie with the given ID exists in the database.

    Args:
        id (int): Movie ID.

    Returns:
        bool: True if the movie exists, False otherwise.
    """
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("SELECT id FROM movies WHERE id=?", (id,))
        results = cur.fetchone()

    return bool(results)


@app.get("/movies", response_model=list[MovieOut], status_code=200)
def get_all_movies():
    """Retrieves all movies from the database.

    Returns:
        list: List of all movies in the database.
    """
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("SELECT id, title, director, category, year FROM movies")
        results = cur.fetchall()

    results = convert_results(results)
    return results


@app.get("/movies/{movie_id}", response_model=MovieOut, status_code=200)
def get_movie_by_id(movie_id: int):
    """Retrieves a specific movie by its ID.

    Args:
        movie_id (int): ID of the movie to retrieve.

    Raises:
        HTTPException: If the movie is not found.

    Returns:
        dict: Movie data.
    """
    if not does_movie_with_id_exist(movie_id):
        raise HTTPException(status_code=404, detail="Movie not found")

    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(
            "SELECT id, title, director, category, year FROM movies WHERE id=?",
            (movie_id,),
        )
        result = cur.fetchone()

    result = convert_result(result)
    return result


@app.post("/movies", status_code=201)
def add_movie(new_movie: MovieIn):
    """Adds a new movie to the database.

    Args:
        new_movie (MovieIn): Movie data to insert.

    Returns:
        dict: Success message.
    """
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO movies (title, director, category, year) VALUES(?, ?, ?, ?)",
            (new_movie.title, new_movie.director, new_movie.category, new_movie.year),
        )
        con.commit()

    return {"message": "Movie added successfully"}


@app.put("/movies/{movie_id}", status_code=200)
def update_movie_by_id(movie_id: int, new_movie: MovieIn):
    """Updates a movie by its ID.

    Args:
        movie_id (int): ID of the movie to update.
        new_movie (MovieIn): New data for the movie.

    Raises:
        HTTPException: If the movie is not found.

    Returns:
        dict: Success message.
    """
    if not does_movie_with_id_exist(movie_id):
        raise HTTPException(status_code=404, detail="Movie not found")

    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(
            """
                UPDATE movies 
                SET title = ?,
                    director = ?,
                    category = ?,
                    year = ?
                WHERE
                    id = ?
            """,
            (
                new_movie.title,
                new_movie.director,
                new_movie.category,
                new_movie.year,
                movie_id,
            ),
        )
        con.commit()

    return {"message": "Movie updated successfully"}


@app.delete("/movies/{movie_id}", status_code=200)
def del_movie_by_id(movie_id: int):
    """Deletes a movie by its ID.

    Args:
        movie_id (int): ID of the movie to delete.

    Raises:
        HTTPException: If the movie is not found.

    Returns:
        dict: Success message.
    """
    if not does_movie_with_id_exist(movie_id):
        raise HTTPException(status_code=404, detail="Movie not found")

    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("DELETE FROM movies WHERE id=?", (movie_id,))
        con.commit()

    return {"message": "Movie deleted successfully"}

from fastapi import FastAPI, HTTPException
from models.movie_models import MovieIn, MovieOut
from controllers.movie_controller import (
    create_movie,
    read_movies,
    read_movie_by_id,
    update_movie_by_id,
    delete_movie_by_id,
)

app = FastAPI()


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

from fastapi import HTTPException
from sqlmodel import SQLModel, Session, select
from movies.models.movie_models import MovieIn, MovieOut


def convert_results(results):
    """Converts SQL query results into a list of dictionaries.

    Args:
        results (Iterable): SQL query results.

    Returns:
        list: A list of dictionaries with movie data.
    """
    results_arr = []

    for row in results:
        inner_dict = {
            "id": row.id,
            "title": row.title,
            "director": row.director,
            "category": row.category,
            "year": row.year,
        }
        results_arr.append(inner_dict)

    return results_arr


def create_movie(session: Session, new_movie: MovieIn):
    """Inserts a new movie into the database.

    Args:
        new_movie (MovieIn): The movie data to be inserted.
    """
    new_movie = MovieOut(**dict(new_movie))
    session.add(new_movie)
    session.commit()


def read_movies(session: Session):
    """Retrieves all movies from the database.

    Returns:
        list: A list of all movies in dictionary format.
    """
    statement = select(MovieOut)
    results = session.exec(statement)
    return convert_results(results)


def read_movie_by_id(session: Session, id: int):
    """Retrieves a specific movie by its ID.

    Args:
        id (int): The ID of the movie to retrieve.

    Raises:
        HTTPException: If the movie is not found.

    Returns:
        dict: Movie data.
    """
    statement = select(MovieOut).where(MovieOut.id == id)
    results = session.exec(statement)

    results = convert_results(results)

    if not results:
        raise HTTPException(status_code=404, detail="Movie not found")

    results = results[0]

    return results


def update_movie_by_id(session: Session, id: int, new_movie: MovieIn):
    """Updates an existing movie by its ID.

    Args:
        id (int): The ID of the movie to update.
        new_movie (MovieIn): The updated movie data.

    Raises:
        HTTPException: If the movie is not found.
    """
    if not read_movie_by_id(session, id):
        raise HTTPException(status_code=404, detail="Movie not found")

    statement = select(MovieOut).where(MovieOut.id == id)
    results = session.exec(statement)

    movie = results.one()

    movie.title = new_movie.title
    movie.director = new_movie.director
    movie.category = new_movie.category
    movie.year = new_movie.year

    session.add(movie)
    session.commit()


def delete_movie_by_id(session: Session, id):
    """Deletes a movie by its ID.

    Args:
        id (int): The ID of the movie to delete.

    Raises:
        HTTPException: If the movie is not found.
    """
    if not read_movie_by_id(session, id):
        raise HTTPException(status_code=404, detail="Movie not found")

    statement = select(MovieOut).where(MovieOut.id == id)
    results = session.exec(statement)

    movie = results.one()

    session.delete(movie)
    session.commit()

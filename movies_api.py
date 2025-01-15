import sqlite3
from typing import Annotated
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()

TABLE_HEADERS = ["id", "title", "director", "category", "year"]
DATABASE = "movies.db"


class MovieBase(BaseModel):
    title: str = Field(min_length=1, description="The title cannot be empty")
    director: str = Field(min_length=1, description="The director cannot be empty")
    category: str = Field(min_length=1, description="The category cannot be empty")
    year: int = Field(gt=0, description="The year must be a positive integer")


class MovieOut(MovieBase):
    id: int


class MovieIn(MovieBase):
    pass


def convert_results(results):
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
    result_dict = {}
    i = 0

    for header in TABLE_HEADERS:
        result_dict[header] = result[i]
        i += 1

    return result_dict


def convert_to_set_of_ids(results):
    results_set = set()

    for tup in results:
        results_set.add(tup[0])

    return results_set


def get_set_of_existing_ids():
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("SELECT id FROM movies")
        results = cur.fetchall()

    results = convert_to_set_of_ids(results)

    return results


def does_movie_with_id_exist(id):
    results = get_set_of_existing_ids()

    if id in results:
        return True

    return False


@app.get("/movies", response_model=list[MovieOut], status_code=200)
def get_all_movies():
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("SELECT id, title, director, category, year FROM movies")
        results = cur.fetchall()

    results = convert_results(results)
    return results


@app.get("/movies/{movie_id}", response_model=MovieOut, status_code=200)
def get_movie_by_id(movie_id: int):
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
    if not does_movie_with_id_exist(movie_id):
        raise HTTPException(status_code=404, detail="Movie not found")

    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("DELETE FROM movies WHERE id=?", (movie_id,))
        con.commit()

    return {"message": "Movie deleted successfully"}

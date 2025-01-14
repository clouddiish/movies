import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

TABLE_HEADERS = ["id", "title", "director", "category", "year"]
DATABASE = "movies.db"


class MovieOut(BaseModel):
    id: int
    title: str
    director: str
    category: str
    year: int


class MovieIn(BaseModel):
    title: str
    director: str
    category: str
    year: int


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


@app.get("/movies/all/", response_model=list[MovieOut], status_code=200)
async def get_all_movies():
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("SELECT rowid, title, director, category, year FROM movies")
        results = cur.fetchall()

    results = convert_results(results)
    return results


@app.get("/movies/{movie_id}/", response_model=MovieOut, status_code=200)
async def get_movie_by_id(movie_id: int):
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(
            "SELECT rowid, title, director, category, year FROM movies WHERE rowid=?",
            (movie_id,),
        )
        result = cur.fetchone()

    result = convert_result(result)
    return result


@app.post("/movies/add/", status_code=201)
async def add_movie(new_movie: MovieIn):
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO movies VALUES(?, ?, ?, ?)",
            (new_movie.title, new_movie.director, new_movie.category, new_movie.year),
        )
        con.commit()

    return {"message": "Movie added successfully"}


@app.put("/movies/edit/{movie_id}/", status_code=200)
async def update_movie_by_id(movie_id: int, new_movie: MovieIn):
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
                    rowid = ?
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


@app.delete("/movies/del/{movie_id}/", status_code=200)
async def del_movie_by_id(movie_id: int):
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("DELETE FROM movies WHERE rowid=?", (movie_id,))
        con.commit()

    return {"message": "Movie deleted successfully"}

import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

TABLE_HEADERS = ["id", "title", "director", "category", "year"]


class Movie(BaseModel):
    id: int
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


@app.get("/movies/all/", response_model=list[Movie], status_code=200)
async def get_all_movies():
    with sqlite3.connect("movies.db") as con:
        cur = con.cursor()
        cur.execute("SELECT rowid, title, director, category, year FROM movies")
        results = cur.fetchall()

    results = convert_results(results)
    return results


@app.get("/movies/{movie_id}", response_model=Movie, status_code=200)
async def get_movie_by_id(movie_id: int):
    with sqlite3.connect("movies.db") as con:
        cur = con.cursor()
        cur.execute(
            "SELECT rowid, title, director, category, year FROM movies WHERE rowid=?",
            (movie_id,),
        )
        result = cur.fetchone()

    result = convert_result(result)
    return result

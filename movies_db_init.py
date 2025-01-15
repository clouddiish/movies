import sqlite3

con = sqlite3.connect("movies.db")
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS movies")
table = """CREATE TABLE movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL, 
            director TEXT NOT NULL,
            category TEXT NOT NULL,
            year INTEGER NOT NULL
            )
        """
cur.execute(table)

initial_data = [
    ("Amazing Movie", "Anne Bee", "action", 1996),
    ("Fantastic Film", "Cee Dee", "sci-fi", 2013),
    ("Epic Adventure", "John Doe", "adventure", 2005),
    ("Mystery Night", "Jane Smith", "mystery", 2010),
    ("Galactic Quest", "Leo King", "sci-fi", 2018),
    ("Silent Shadows", "Mia Moon", "thriller", 2002),
    ("Romantic Escape", "Ella Rose", "romance", 2015),
    ("Crimson Tide", "Mark Steel", "action", 1999),
    ("Frozen Echoes", "Nina Frost", "drama", 2020),
    ("Hidden Truth", "Oscar Vale", "mystery", 2007),
    ("Twilight Chase", "Paul Knight", "thriller", 2012),
    ("Velvet Horizon", "Quinn Blue", "fantasy", 2019),
    ("Blazing Fury", "Rex Blaze", "action", 2001),
    ("Echoes of Time", "Sophie Lane", "sci-fi", 2017),
    ("Golden Mirage", "Tommy Rivers", "adventure", 2003),
]

cur.executemany(
    "INSERT INTO movies (title, director, category, year) VALUES(?, ?, ?, ?)",
    initial_data,
)
con.commit()

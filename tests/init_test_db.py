from sqlmodel import create_engine, SQLModel, Session
from sqlmodel.pool import StaticPool
from ex6.models.movie_models import MovieOut

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def create_initial_movies():
    initial_data = [
        MovieOut(
            title="Amazing Movie", director="Anne Bee", category="action", year=1996
        ),
        MovieOut(
            title="Fantastic Film", director="Cee Dee", category="sci-fi", year=2013
        ),
        MovieOut(
            title="Epic Adventure", director="John Doe", category="adventure", year=2005
        ),
        MovieOut(
            title="Mystery Night", director="Jane Smith", category="mystery", year=2010
        ),
        MovieOut(
            title="Galactic Quest", director="Leo King", category="sci-fi", year=2018
        ),
        MovieOut(
            title="Silent Shadows", director="Mia Moon", category="thriller", year=2002
        ),
        MovieOut(
            title="Romantic Escape", director="Ella Rose", category="romance", year=2015
        ),
        MovieOut(
            title="Crimson Tide", director="Mark Steel", category="action", year=1999
        ),
        MovieOut(
            title="Frozen Echoes", director="Nina Frost", category="drama", year=2020
        ),
        MovieOut(
            title="Hidden Truth", director="Oscar Vale", category="mystery", year=2007
        ),
        MovieOut(
            title="Twilight Chase",
            director="Paul Knight",
            category="thriller",
            year=2012,
        ),
        MovieOut(
            title="Velvet Horizon", director="Quinn Blue", category="fantasy", year=2019
        ),
        MovieOut(
            title="Blazing Fury", director="Rex Blaze", category="action", year=2001
        ),
        MovieOut(
            title="Echoes of Time", director="Sophie Lane", category="sci-fi", year=2017
        ),
        MovieOut(
            title="Golden Mirage",
            director="Tommy Rivers",
            category="adventure",
            year=2003,
        ),
    ]

    with Session(engine) as session:
        for movie in initial_data:
            session.add(movie)

        session.commit()


def main():
    create_db_and_tables()
    create_initial_movies()


if __name__ == "__main__":
    main()

from sqlmodel import create_engine, Session

# Construct the SQLite database URL
sqlite_url = "sqlite:///./movies/db/movies.db"

# Create the SQLAlchemy engine using the SQLite URL
engine = create_engine(sqlite_url)


def get_session():
    with Session(engine) as session:
        yield session

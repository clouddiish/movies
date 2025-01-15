from sqlmodel import create_engine

sqlite_file_name = "movies.db"
sqlite_url = f"sqlite:///db/{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

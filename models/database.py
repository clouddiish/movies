from sqlmodel import create_engine

# Define the SQLite database file name
sqlite_file_name = "movies.db"

# Construct the SQLite database URL
sqlite_url = f"sqlite:///db/{sqlite_file_name}"

# Create the SQLAlchemy engine using the SQLite URL
engine = create_engine(sqlite_url)
"""
Initializes the SQLAlchemy engine for the SQLite database.

Attributes:
    sqlite_file_name (str): The name of the SQLite database file.
    sqlite_url (str): The SQLite URL used to connect to the database.
    engine (Engine): The SQLAlchemy engine object for database operations.
"""

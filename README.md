# movies API

Movies API is a `FastAPI` REST API for managing a SQLite movie database. It allows to create, read, update, and delete movies, using `SQLModel` for database interactions. The API includes unit tests for core functionalities.

## features

- **read all movies** - fetch a list of all movies in the database
- **read a specific movie by ID** - fet details of a movie using its ID
- **add a new movie** -iInsert a new movie into the database
- **update an existing movie** - modify the details of a specific movie using its ID
- **delete a movie** - remove a movie from the database by its ID

## getting started

### dependencies

- Python 3.8 or later
- Python packages from `requirements.txt`
```
pip install -r requirements.txt
```

### installation

- clone the repository or download the code files

### run

- enter the root directory of the application
- start the application with the below command
```
fastapi dev movies\main.py   
```

### output 

- view the interactive docs at http://127.0.0.1:8000/docs

### run tests

- run the tests with the below command
```
pytest
```


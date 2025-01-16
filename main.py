from fastapi import FastAPI
from ex6.routes.movie_routes import router

app = FastAPI()
"""
Initializes the FastAPI application and includes the movie routes.

Attributes:
    app (FastAPI): The FastAPI application instance used to define API routes and configurations.
"""

app.include_router(router)
"""
Includes the movie router to register movie-related endpoints with the FastAPI app.

Args:
    router (APIRouter): Router instance containing all movie-related routes.
"""

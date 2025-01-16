from fastapi import FastAPI
from ex6.routes.movie_routes import router

app = FastAPI()

app.include_router(router)

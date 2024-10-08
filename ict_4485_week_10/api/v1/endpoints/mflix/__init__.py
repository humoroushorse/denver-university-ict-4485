"""FastAPI route definitions."""
from fastapi import APIRouter
from ict_4485_week_10.api.v1.endpoints.mflix import (
  comments, 
  # embeded_movies, 
  movies,
  sessions,
  theaters,
  users
)

router = APIRouter()

router.include_router(comments.router, prefix="/comments", tags=["Comments"])
# router.include_router(embeded_movies.router, prefix="/embedded-movies", tags=["Embedded Movies"])
router.include_router(movies.router, prefix="/movies", tags=["Movies"])
router.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
router.include_router(theaters.router, prefix="/theaters", tags=["Theaters"])
router.include_router(users.router, prefix="/users", tags=["Users"])

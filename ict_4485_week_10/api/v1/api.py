"""FastAPI route definitions."""

from ict_4485_week_10.api.v1.endpoints import info, mflix
from fastapi import APIRouter

api_router = APIRouter()

# api_router.include_router(login.router, tags=["login"])
api_router.include_router(info.router, prefix="/info", tags=["API Info"])
api_router.include_router(mflix.router, prefix="/mflix", tags=["MFlix"])

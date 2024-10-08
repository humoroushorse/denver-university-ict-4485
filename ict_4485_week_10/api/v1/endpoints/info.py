"""API Info."""

from fastapi import APIRouter
from ict_4485_week_10.config import get_settings

router = APIRouter()

@router.get("/")
async def get_info():
    return get_settings().model_dump(exclude={'mongo_password'})

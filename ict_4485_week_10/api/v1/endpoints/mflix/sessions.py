from typing import List, Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReadPreference
from loguru import logger

from ict_4485_week_10.models import session_models, db_models
from ict_4485_week_10.db.lifespan import get_mongo_db, MongoDatabase


router = APIRouter()

@router.get(
    '/',
    response_model=List[session_models.SessionReadModel],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {}
    }
)
async def get_sessions(
    db: Annotated[MongoDatabase | None, Depends(get_mongo_db)],
    skip: int = 0, 
    limit: int = 100, 
):
    if db:
        try:
            client: AsyncIOMotorClient = db.client
            db = client.get_database(db_models.DbNameEnum.SAMPLE_MFLIX.value)
            collection = db.get_collection(db_models.SampleMflixNameEnum.SESSIONS.value, read_preference=ReadPreference.SECONDARY)
            cursor = collection.find().limit(limit).skip(skip)
            sessions: List[session_models.SessionReadModel] = await cursor.to_list(length=None)
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return sessions
    else:
        raise Exception("Failed to connect to database.")
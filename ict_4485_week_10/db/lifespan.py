import fastapi
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from ict_4485_week_10.config import get_settings, Settings


def get_db_client(settings: Settings) -> AsyncIOMotorClient:
  uri = f"mongodb+srv://{settings.mongo_username}:{settings.mongo_password}@{settings.mongo_db_name}.rix82.mongodb.net/"
  logger.info("uri=%s", uri.replace(settings.mongo_password, "******"))
  # Set the Stable API version when creating a new client
  client = AsyncIOMotorClient(uri, server_api=ServerApi(str(settings.mongo_api_version)))
  return client


class MongoDatabase:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            settings = get_settings()
            cls.instance = super().__new__(cls)
            cls.instance.client = get_db_client(settings)
            cls.instance.default_db = cls.instance.client.get_default_database(settings.mongo_default_db_name)
        return cls.instance


async def get_mongo_db() -> MongoDatabase | None:
    return MongoDatabase()


async def db_lifespan(app: fastapi.FastAPI):
    # Startup
    db = await get_mongo_db()
    ping_response = await db.default_db.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        logger.info("Connected to database cluster.")
    yield

    # Shutdown
    db.client.close()
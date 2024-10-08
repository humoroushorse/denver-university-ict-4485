import fastapi
import uvicorn
from loguru import logger
from ict_4485_week_10.config import get_settings
from ict_4485_week_10.api.v1.api import api_router
from ict_4485_week_10.db.lifespan import db_lifespan

app = fastapi.FastAPI(lifespan=db_lifespan)
app.include_router(api_router, prefix=get_settings().api_v1_base)


def setup_logging():
  log_level = 'INFO'
  logger.add(
      "logs/{time}.log",
      format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
      rotation="1 day",
      retention="10 days",
      level=log_level,
  )
  logger.debug("This is a debug log!")
  logger.info("This is a info log!")
  logger.success("This is a success log!")
  logger.warning("This is a warning log!")
  logger.error("This is a error log!")
  logger.critical("This is a critical log!")
  logger.exception("This is a exception log!")


if __name__ == "__main__":
    setup_logging()
    settings = get_settings()
    logger.info(f"Docs found at http://{settings.api_host}:{settings.api_port}/docs")
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)


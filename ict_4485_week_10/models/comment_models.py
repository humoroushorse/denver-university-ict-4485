from pydantic import BaseModel, EmailStr, Field, AliasChoices
import datetime
from ict_4485_week_10.models import core_models

class CommentEntity(core_models.BaseModelWithId):
  name: str
  email: EmailStr
  movie_id: str
  text: str
  date: datetime.datetime

class CommentReadModel(CommentEntity):
  email: int = Field(exclude=True)

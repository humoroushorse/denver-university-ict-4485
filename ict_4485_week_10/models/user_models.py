from pydantic import BaseModel, EmailStr, Field, AliasChoices, field_validator
from loguru import logger
from typing import Any
import bson
from ict_4485_week_10.models import core_models


class UserEntity(core_models.BaseModelWithId):
  name: str
  email: EmailStr
  password: str

  @field_validator("id", mode="before")
  @classmethod
  def transform_id(cls, data: bson.objectid.ObjectId) -> Any:
    return str(data)


class UserReadModel(UserEntity):
  email: EmailStr = Field(exclude=True)
  password: str = Field(exclude=True)


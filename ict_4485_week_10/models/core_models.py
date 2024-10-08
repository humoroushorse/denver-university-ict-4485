from pydantic import BaseModel, Field, AliasChoices, field_validator
import bson


class BaseModelWithId(BaseModel):
  id: str = Field(validation_alias=AliasChoices("_id", "id"))

  @field_validator("id", mode="before")
  @classmethod
  def transform_id(cls, data: bson.objectid.ObjectId) -> str:
    return str(data)
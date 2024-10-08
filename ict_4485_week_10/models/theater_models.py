from pydantic import BaseModel
from ict_4485_week_10.models import core_models

class TheaterLocationAddress(BaseModel):
    street1: str
    city: str
    state: str
    zipcode: str

class TheaterLocationGeo(BaseModel):
    type: str
    coordinates: list[float]

class TheaterLocation(BaseModel):
    address: TheaterLocationAddress
    geo: TheaterLocationGeo

class TheaterEntity(core_models.BaseModelWithId):
    theaterId: int
    location: TheaterLocation


class TheaterReadModel(TheaterEntity):
    pass

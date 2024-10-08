from __future__ import annotations

from typing import List
import datetime

from pydantic import BaseModel, Field, field_validator
from ict_4485_week_10.models import core_models

class MovieTomatoesViewerCritic(BaseModel):
    rating: int | None = Field(default=None)
    numReviews: int | None = Field(default=None)
    meter: int | None = Field(default=None)

    @field_validator("rating", "numReviews", "meter", mode="before")
    @classmethod
    def transform_ints(cls, data) -> int | None:
        return int(data) if data else None

class MovieTomatoes(BaseModel):
    website: str | None = Field(default=None)
    viewer: MovieTomatoesViewerCritic | None = Field(default=None)
    critic: MovieTomatoesViewerCritic | None = Field(default=None)
    dvd: datetime.datetime | None = Field(default=None)
    boxOffice: str | None = Field(default=None)
    concensus: str | None = Field(default=None)
    rotten: int | None = Field(default=None)
    production: str | None = Field(default=None)
    lastUpdated: datetime.datetime | None = Field(default=None)
    fresh: int | None = Field(default=None)

    @field_validator("rotten", "fresh", mode="before")
    @classmethod
    def transform_ints(cls, data) -> int | None:
        return int(data) if data else None

class MovieImdb(BaseModel):
    # rating: int = Field(validation_alias=AliasChoices(AliasPath(["rating", "$numberDouble"]), "rating"))
    rating: float | None = Field(default=None)
    # votes: int = Field(validation_alias=AliasChoices(AliasPath(["votes", "$numberInt"]), "votes"))
    votes: int | None = Field(default=None)
    # id: int = Field(validation_alias=AliasChoices(AliasPath(["id", "$numberInt"]), "id"))
    id: int | None = Field(default=None)

    @field_validator("rating", mode="before")
    @classmethod
    def transform_floats(cls, data) -> float | None:
        return float(data) if data else None

    @field_validator("votes", "id", mode="before")
    @classmethod
    def transform_ints(cls, data) -> int | None:
        return int(data) if data else None

class MovieAwards(BaseModel):
    # wins: int = Field(validation_alias=AliasChoices(AliasPath(["wins", "$numberInt"]), "wins"))
    wins: int | None = Field(default=None)
    # nominations: int = Field(validation_alias=AliasChoices(AliasPath(["nominations", "$numberInt"]), "nominations"))
    nominations: int | None = Field(default=None)
    text: str | None = Field(default=None)

    @field_validator("nominations", "wins", mode="before")
    @classmethod
    def transform_ints(cls, data) -> int | None:
        return int(data) if data else None

class MovieEntity(core_models.BaseModelWithId):
    plot: str | None = Field(default=None)
    genres: List[str] | None = Field(default=None)
    # runtime: int = Field(validation_alias=AliasChoices(AliasPath(["runtime", "$numberInt"]), "runtime"))
    runtime: int | None = Field(default=None)
    cast: List[str] | None = Field(default=None)
    # num_mflix_comments: int = Field(validation_alias=AliasChoices(AliasPath(["runtime", "$numberLong"]), "runtime"))
    num_mflix_comments: int
    title: str
    fullplot: str | None = Field(default=None)
    languages: List[str] | None = Field(default_factory=list)
    released: datetime.datetime | None = None
    directors: List[str] | None = Field(default=None)
    rated: str | None = Field(default=None)
    awards: MovieAwards
    lastupdated: str
    # year: int = Field(validation_alias=AliasChoices(AliasPath(["year", "$numberInt"]), "year"))
    # note some of the years are like 2014è so it has to allow string...
    year: int | str
    imdb: MovieImdb
    countries: List[str] | None = Field(default=None)
    type: str
    tomatoes: MovieTomatoes | None = Field(default=None)

class MoveReadModel(MovieEntity):
    pass

class MoveTopRatedImdbModel(core_models.BaseModelWithId):
    title: str
    imdb: MovieImdb

class MoveTopRatedImdbCastModel(core_models.BaseModelWithId):
    title: str
    imdb: MovieImdb
    cast: List[str]

class MoveTopRatedImdbDirectorsModel(core_models.BaseModelWithId):
    title: str
    imdb: MovieImdb
    directors: List[str]

class MovieTomatoesOnlyRottenFresh(BaseModel):
    rotten: int | None = Field(default=None)
    fresh: int | None = Field(default=None)

    @field_validator("rotten", "fresh", mode="before")
    @classmethod
    def transform_ints(cls, data) -> int | None:
        return int(data) if data else None

class MoveTopRatedTomatoesModel(core_models.BaseModelWithId):
    title: str
    tomatoes: MovieTomatoesOnlyRottenFresh | None = Field(default=None)

class MoveTopRatedTomatoesCastModel(core_models.BaseModelWithId):
    title: str
    tomatoes: MovieTomatoesOnlyRottenFresh | None = Field(default=None)
    cast: List[str]

class MoveTopRatedTomatoesDirectorsModel(core_models.BaseModelWithId):
    title: str
    tomatoes: MovieTomatoesOnlyRottenFresh | None = Field(default=None)
    directors: List[str]
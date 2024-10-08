from enum import Enum
import pymongo
from typing import Literal

class DbNameEnum(str, Enum):
    DEFAULT = "sample_mflix"
    SAMPLE_MFLIX = "sample_mflix"

class SampleMflixNameEnum(str, Enum):
    COMMENTS = "comments"
    EMBEDDED_MOVIES = "embedded_movies"
    MOVIES = "movies"
    SESSIONS = "sessions"
    THEATERS = "theaters"
    USERS = "users"

class DbSortEnum(str, Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"

def map_sort_enum(enum: DbSortEnum) -> Literal[1] | Literal[-1] :
    if enum == DbSortEnum.ASCENDING:
        return pymongo.ASCENDING
    return pymongo.DESCENDING
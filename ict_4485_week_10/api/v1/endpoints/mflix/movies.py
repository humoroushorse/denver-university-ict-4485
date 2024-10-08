from typing import List, Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
import pymongo
import re
from loguru import logger
import pymongo.collection

from ict_4485_week_10.models import movie_models, db_models
from ict_4485_week_10.db.lifespan import get_mongo_db, MongoDatabase


router = APIRouter()


@router.get(
    "/",
    response_model=List[movie_models.MoveReadModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {}},
)
async def get_movies(
    db: Annotated[MongoDatabase | None, Depends(get_mongo_db)],
    skip: int = 0,
    limit: int = 100,
):
    if db:
        try:
            client: AsyncIOMotorClient = db.client
            db = client.get_database(db_models.DbNameEnum.SAMPLE_MFLIX.value)
            collection = db.get_collection(
                db_models.SampleMflixNameEnum.MOVIES.value,
                read_preference=pymongo.ReadPreference.SECONDARY,
            )
            cursor = collection.find().limit(limit).skip(skip)
            movies: List[movie_models.MoveReadModel] = await cursor.to_list(length=None)
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return movies
    else:
        raise Exception("Failed to connect to database.")


@router.get(
    "/top-rated-imdb",
    response_model=List[movie_models.MoveTopRatedImdbModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {}},
    description="Get all of the top movies by IMDB rating, movies with no rating are rated at 0",
)
async def get_movies_top_rated_imdb(
    db: Annotated[MongoDatabase | None, Depends(get_mongo_db)],
    sort: db_models.DbSortEnum = db_models.DbSortEnum.DESCENDING,
    skip: int = 0,
    limit: int = 100,
    # sort: db_models.DbSortEnum = db_models.DbSortEnum.DESCENDING.value
):
    if db:
        try:
            client: AsyncIOMotorClient = db.client
            db = client.get_database(db_models.DbNameEnum.SAMPLE_MFLIX.value)
            collection: AsyncIOMotorCollection = db.get_collection(
                db_models.SampleMflixNameEnum.MOVIES.value,
                read_preference=pymongo.ReadPreference.SECONDARY,
            )
            aggregate = [
                {
                    "$addFields": {
                        "__rating_value": {
                            "$cond": {
                                "if": {
                                    "$or": [
                                        {"$eq": ["$imdb.rating", ""]},
                                        {"$eq": ["$imdb.rating", None]},
                                    ]
                                },
                                "then": 0,
                                "else": {"$toDouble": "$imdb.rating"},
                            }
                        }
                    }
                },
                {"$sort": {"__rating_value": db_models.map_sort_enum(sort)}},
                {"$skip": skip},
            ]
            if limit:
                aggregate.append({"$limit": limit})
            # allowDiskUse is True because of memory issues when user doesn't provide a limit
            #    TODO: optimize query or at least create indexes...
            #    that said, it still does the memory issue (probably free tier?)
            cursor = collection.aggregate(aggregate, allowDiskUse=True)
            movies: List[movie_models.MoveTopRatedImdbModel] = await cursor.to_list(
                length=None
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return movies
    else:
        raise Exception("Failed to connect to database.")



@router.get(
    "/top-rated-imdb-by-cast",
    response_model=List[movie_models.MoveTopRatedImdbCastModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {}},
    description="Get all of the top movies by IMDB rating for a given cast member, movies with no rating are rated at 0",
)
async def get_movies_top_rated_imdb_cast(
    db: Annotated[MongoDatabase | None, Depends(get_mongo_db)],
    actor_name: str,
    sort: db_models.DbSortEnum = db_models.DbSortEnum.DESCENDING,
    skip: int = 0,
    limit: int = 100,
    # sort: db_models.DbSortEnum = db_models.DbSortEnum.DESCENDING.value
):
    if db:
        try:
            client: AsyncIOMotorClient = db.client
            db = client.get_database(db_models.DbNameEnum.SAMPLE_MFLIX.value)
            collection: AsyncIOMotorCollection = db.get_collection(
                db_models.SampleMflixNameEnum.MOVIES.value,
                read_preference=pymongo.ReadPreference.SECONDARY,
            )
            aggregate = [
                {  "$match": {
                    "cast": {
                        "$regex": re.compile(actor_name.strip(), re.IGNORECASE)
                    }
                  }
                },
                {
                    "$addFields": {
                        "__rating_value": {
                            "$cond": {
                                "if": {
                                    "$or": [
                                        {"$eq": ["$imdb.rating", ""]},
                                        {"$eq": ["$imdb.rating", None]},
                                    ]
                                },
                                "then": 0,
                                "else": {"$toDouble": "$imdb.rating"},
                            }
                        }
                    }
                },
                {"$sort": {"__rating_value": db_models.map_sort_enum(sort)}},
                {"$skip": skip},
            ]
            if limit:
                aggregate.append({"$limit": limit})
            # allowDiskUse is True because of memory issues when user doesn't provide a limit
            #    TODO: optimize query or at least create indexes...
            #    that said, it still does the memory issue (probably free tier?)
            cursor = collection.aggregate(aggregate, allowDiskUse=True)
            movies: List[movie_models.MoveTopRatedImdbCastModel] = await cursor.to_list(
                length=None
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return movies
    else:
        raise Exception("Failed to connect to database.")



@router.get(
    "/top-rated-imdb-by-director",
    response_model=List[movie_models.MoveTopRatedImdbDirectorsModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {}},
    description="Get all of the top movies by IMDB rating for a given director, movies with no rating are rated at 0",
)
async def get_movies_top_rated_imdb_directors(
    db: Annotated[MongoDatabase | None, Depends(get_mongo_db)],
    director_name: str,
    sort: db_models.DbSortEnum = db_models.DbSortEnum.DESCENDING,
    skip: int = 0,
    limit: int = 100,
    # sort: db_models.DbSortEnum = db_models.DbSortEnum.DESCENDING.value
):
    if db:
        try:
            client: AsyncIOMotorClient = db.client
            db = client.get_database(db_models.DbNameEnum.SAMPLE_MFLIX.value)
            collection: AsyncIOMotorCollection = db.get_collection(
                db_models.SampleMflixNameEnum.MOVIES.value,
                read_preference=pymongo.ReadPreference.SECONDARY,
            )
            aggregate = [
                {  "$match": {
                    "directors": {
                        "$regex": re.compile(director_name.strip(), re.IGNORECASE)
                    }
                  }
                },
                {
                    "$addFields": {
                        "__rating_value": {
                            "$cond": {
                                "if": {
                                    "$or": [
                                        {"$eq": ["$imdb.rating", ""]},
                                        {"$eq": ["$imdb.rating", None]},
                                    ]
                                },
                                "then": 0,
                                "else": {"$toDouble": "$imdb.rating"},
                            }
                        }
                    }
                },
                {"$sort": {"__rating_value": db_models.map_sort_enum(sort)}},
                {"$skip": skip},
            ]
            if limit:
                aggregate.append({"$limit": limit})
            # allowDiskUse is True because of memory issues when user doesn't provide a limit
            #    TODO: optimize query or at least create indexes...
            #    that said, it still does the memory issue (probably free tier?)
            cursor = collection.aggregate(aggregate, allowDiskUse=True)
            movies: List[movie_models.MoveTopRatedImdbDirectorsModel] = await cursor.to_list(
                length=None
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return movies
    else:
        raise Exception("Failed to connect to database.")


@router.get(
    "/top-rated-tomatoes-fresh",
    response_model=List[movie_models.MoveTopRatedTomatoesModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {}},
    description="Get all of the top movies by Rotten Tomatoes Freshness rating, movies with no rating are rated at 0",
)
async def get_movies_top_rated_tomatoes_fresh(
    db: Annotated[MongoDatabase | None, Depends(get_mongo_db)],
    sort: db_models.DbSortEnum = db_models.DbSortEnum.DESCENDING,
    skip: int = 0,
    limit: int = 100,
    # sort: db_models.DbSortEnum = db_models.DbSortEnum.DESCENDING.value
):
    if db:
        try:
            client: AsyncIOMotorClient = db.client
            db = client.get_database(db_models.DbNameEnum.SAMPLE_MFLIX.value)
            collection: AsyncIOMotorCollection = db.get_collection(
                db_models.SampleMflixNameEnum.MOVIES.value,
                read_preference=pymongo.ReadPreference.SECONDARY,
            )
            aggregate = [
                {
                    "$addFields": {
                        "__rating_value": {
                            "$cond": {
                                "if": {
                                    "$or": [
                                        {"$eq": ["$tomatoes.fresh", ""]},
                                        {"$eq": ["$tomatoes.fresh", None]},
                                    ]
                                },
                                "then": 0,
                                "else": {"$toDouble": "$tomatoes.fresh"},
                            }
                        }
                    }
                },
                {"$sort": {"__rating_value": db_models.map_sort_enum(sort)}},
                {"$skip": skip},
            ]
            if limit:
                aggregate.append({"$limit": limit})
            # allowDiskUse is True because of memory issues when user doesn't provide a limit
            #    TODO: optimize query or at least create indexes...
            #    that said, it still does the memory issue (probably free tier?)
            cursor = collection.aggregate(aggregate, allowDiskUse=True)
            movies: List[movie_models.MoveTopRatedTomatoesModel] = await cursor.to_list(
                length=None
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return movies
    else:
        raise Exception("Failed to connect to database.")

@router.get(
    "/top-rated-tomatoes-fresh-by-cast",
    response_model=List[movie_models.MoveTopRatedTomatoesCastModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {}},
    description="Get all of the top movies by Rotten Tomatoes Freshness rating by cast member, movies with no rating are rated at 0",
)
async def get_movies_top_rated_tomatoes_fresh_by_cast(
    db: Annotated[MongoDatabase | None, Depends(get_mongo_db)],
    actor_name: str,
    sort: db_models.DbSortEnum = db_models.DbSortEnum.DESCENDING,
    skip: int = 0,
    limit: int = 100,
    # sort: db_models.DbSortEnum = db_models.DbSortEnum.DESCENDING.value
):
    if db:
        try:
            client: AsyncIOMotorClient = db.client
            db = client.get_database(db_models.DbNameEnum.SAMPLE_MFLIX.value)
            collection: AsyncIOMotorCollection = db.get_collection(
                db_models.SampleMflixNameEnum.MOVIES.value,
                read_preference=pymongo.ReadPreference.SECONDARY,
            )
            aggregate = [
                {  "$match": {
                    "cast": {
                        "$regex": re.compile(actor_name.strip(), re.IGNORECASE)
                    }
                  }
                },
                {
                    "$addFields": {
                        "__rating_value": {
                            "$cond": {
                                "if": {
                                    "$or": [
                                        {"$eq": ["$tomatoes.fresh", ""]},
                                        {"$eq": ["$tomatoes.fresh", None]},
                                    ]
                                },
                                "then": 0,
                                "else": {"$toDouble": "$tomatoes.fresh"},
                            }
                        }
                    }
                },
                {"$sort": {"__rating_value": db_models.map_sort_enum(sort)}},
                {"$skip": skip},
            ]
            if limit:
                aggregate.append({"$limit": limit})
            # allowDiskUse is True because of memory issues when user doesn't provide a limit
            #    TODO: optimize query or at least create indexes...
            #    that said, it still does the memory issue (probably free tier?)
            cursor = collection.aggregate(aggregate, allowDiskUse=True)
            movies: List[movie_models.MoveTopRatedTomatoesCastModel] = await cursor.to_list(
                length=None
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return movies
    else:
        raise Exception("Failed to connect to database.")

@router.get(
    "/top-rated-tomatoes-fresh-by-director",
    response_model=List[movie_models.MoveTopRatedTomatoesDirectorsModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {}},
    description="Get all of the top movies by Rotten Tomatoes Freshness rating by director, movies with no rating are rated at 0",
)
async def get_movies_top_rated_tomatoes_fresh_by_director(
    db: Annotated[MongoDatabase | None, Depends(get_mongo_db)],
    director_name: str,
    sort: db_models.DbSortEnum = db_models.DbSortEnum.DESCENDING,
    skip: int = 0,
    limit: int = 100,
    # sort: db_models.DbSortEnum = db_models.DbSortEnum.DESCENDING.value
):
    if db:
        try:
            client: AsyncIOMotorClient = db.client
            db = client.get_database(db_models.DbNameEnum.SAMPLE_MFLIX.value)
            collection: AsyncIOMotorCollection = db.get_collection(
                db_models.SampleMflixNameEnum.MOVIES.value,
                read_preference=pymongo.ReadPreference.SECONDARY,
            )
            aggregate = [
                {  "$match": {
                    "directors": {
                        "$regex": re.compile(director_name.strip(), re.IGNORECASE)
                    }
                  }
                },
                {
                    "$addFields": {
                        "__rating_value": {
                            "$cond": {
                                "if": {
                                    "$or": [
                                        {"$eq": ["$tomatoes.fresh", ""]},
                                        {"$eq": ["$tomatoes.fresh", None]},
                                    ]
                                },
                                "then": 0,
                                "else": {"$toDouble": "$tomatoes.fresh"},
                            }
                        }
                    }
                },
                {"$sort": {"__rating_value": db_models.map_sort_enum(sort)}},
                {"$skip": skip},
            ]
            if limit:
                aggregate.append({"$limit": limit})
            # allowDiskUse is True because of memory issues when user doesn't provide a limit
            #    TODO: optimize query or at least create indexes...
            #    that said, it still does the memory issue (probably free tier?)
            cursor = collection.aggregate(aggregate, allowDiskUse=True)
            movies: List[movie_models.MoveTopRatedTomatoesDirectorsModel] = await cursor.to_list(
                length=None
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return movies
    else:
        raise Exception("Failed to connect to database.")

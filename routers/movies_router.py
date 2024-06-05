from fastapi import APIRouter, HTTPException, status
from pymongo import ReturnDocument
from models.movie import Movie, MovieInDb
from db.database import create_and_validate_objectId, db

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)

collection = db['movies']

@router.get('/', response_model=list[Movie])
async def get_all_movies() -> list[Movie] | None:
    with collection.find() as movies:
        return [Movie(**movie) for movie in movies]

@router.get("/{id}", response_model_by_alias=False)
async def get_movie(id:str) -> Movie | None:
    movie_id = create_and_validate_objectId(id)
    movie = collection.find_one({"_id": movie_id})
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Movie(**movie)

@router.post("/", response_model=Movie, response_model_by_alias=False)
async def create_movie(movie:Movie) -> Movie | None:
    movie_dict = MovieInDb(**(movie.model_dump())).model_dump(by_alias=True, exclude=['id'])
    result = collection.insert_one(movie_dict)
    created_movie = collection.find_one({"_id": result.inserted_id})
    if created_movie is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Movie(**created_movie)

@router.put("/{id}", response_model=Movie, response_model_by_alias=False)
async def update_movie(id:str, movie:Movie) -> Movie | None:
    movie_id = create_and_validate_objectId(id)
    movie_dict = MovieInDb(**(movie.model_dump())).model_dump(by_alias=True, exclude=['id'])
    result = collection.find_one_and_update({"_id": movie_id}, {"$set": movie_dict}, return_document=ReturnDocument.AFTER)
    if result is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Movie(**result)

@router.delete("/{id}")
async def delete_movie(id:str) -> None:
    movie_id = create_and_validate_objectId(id)
    result = collection.delete_one({"_id": movie_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

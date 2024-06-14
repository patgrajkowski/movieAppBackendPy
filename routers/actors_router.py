from fastapi import APIRouter, HTTPException, status
from db.database import create_and_validate_objectId, db
from models.actor import Actor

router = APIRouter(
    prefix='/actors',
    tags=['Actors']
)

collection = db['actors']


@router.get("/", response_model=list[Actor])
async def get_all_actors() -> list[Actor]:
    with collection.find() as actors:
        return [Actor(**actor) for actor in actors]


@router.get("/{id}", response_model=Actor)
async def get_actor(id: str) -> Actor | None:
    actor_id = create_and_validate_objectId(id)
    actor = collection.find_one({'_id': actor_id})
    if actor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Actor(**actor)


@router.post("/", response_model=Actor)
async def add_actor(actor: Actor) -> Actor | None:
    actor_dict = actor.model_dump(by_alias=True, exclude=['id'])
    result = collection.insert_one(actor_dict)
    created_actor = collection.find_one({"_id": result.inserted_id})
    if created_actor is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Actor(**created_actor)


@router.delete("/{id}")
async def delete_actor(id: str) -> None:
    actor_id = create_and_validate_objectId(id)
    result = collection.delete_one({'_id': actor_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

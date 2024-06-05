from fastapi import APIRouter, HTTPException, status
from db.database import create_and_validate_objectId, db
from models.comment import Comment, CommentInDb

router = APIRouter(
    prefix='/comments',
    tags=['Comments']
)

collection = db['comments']

@router.get("/movie/{movie_id}", response_model=list[Comment])
async def get_comments_by_movie(id: str) -> list[Comment] | None:
    movie_id = create_and_validate_objectId(id)
    with collection.find({'movie_id': movie_id}) as comments:
        return list(comments)

@router.get("/user/{user_id}", response_model=list[Comment])
async def get_comments_by_user(id: str) -> list[Comment] | None:
    movie_id = create_and_validate_objectId(id)
    with collection.find({'user_id': movie_id}) as comments:
        return list(comments)


@router.post("/", response_model=Comment)
async def add_comment(comment: Comment) -> Comment | None:
    comment_dict = CommentInDb(**(comment.model_dump())).model_dump(by_alias=True, exclude=['id'])
    result = collection.insert_one(comment_dict)
    created_comment = collection.find_one({'_id': result.inserted_id})
    if created_comment is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Comment(**created_comment)

@router.delete("/{id}")
async def delete_comment(id: str) -> None:
    comment_id = create_and_validate_objectId(id)
    result = collection.delete_one({'_id': comment_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
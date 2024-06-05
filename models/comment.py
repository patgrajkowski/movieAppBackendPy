from typing import Optional
from pydantic import BaseModel, Field;
from datetime import date, datetime
from db.database import PyObjectId;

class BaseComment(BaseModel):
    id: Optional[PyObjectId] = Field(alias = "_id", default = None)
    user_id: str
    movie_id: str
    text: str

class Comment(BaseComment):
    date: date

class CommentInDb(BaseComment):
    date: datetime

    def __init__(self, /, **data):
        super().__init__(**data)
        self.date=datetime.combine(self.date, datetime.min.time())
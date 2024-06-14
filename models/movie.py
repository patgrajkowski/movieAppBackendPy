from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from db.database import PyObjectId

class CastMember(BaseModel):
    actor_id: str
    image: str
    name: str
    role: str

class BaseMovie(BaseModel):
    id: Optional[PyObjectId] = Field(alias = "_id", default = None)
    title: str
    plot: str
    runtime: int
    genres: List[str]
    cast: List[CastMember]
    directors: List[str]
    type: Literal['movie', 'series']
    images: List[str]
    comments: List[str] = Field(description='List of comments IDs')

class Movie(BaseMovie):
    release_date: date

class MovieInDb(BaseMovie):
    release_date: datetime

    def __init__(self, /, **data):
        super().__init__(**data)
        self.release_date=datetime.combine(self.release_date, datetime.min.time())
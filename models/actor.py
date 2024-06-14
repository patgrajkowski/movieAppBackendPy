from typing import List, Optional
from pydantic import BaseModel, Field
from db.database import PyObjectId


class Actor(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    first_name: str
    last_name: str
    description: str
    images: List[str]
    starred_in: Optional[List[str]]

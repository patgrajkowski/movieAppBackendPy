import os, sys
from typing import Annotated
from bson import ObjectId
from fastapi import HTTPException, status
from pydantic import BeforeValidator
from pymongo import MongoClient;

PyObjectId = Annotated[str, BeforeValidator(str)]

try:
    client = MongoClient(os.environ['MONGO_URL']);
    db = client.filmly;
except:
    print("MONGO_URL env variable need to be set")
    sys.exit()



def create_and_validate_objectId(id: str) -> str | None:
    try:
        return ObjectId(id)
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
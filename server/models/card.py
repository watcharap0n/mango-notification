from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from db import PyObjectId


class Card(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    card: Optional[str] = None
    description: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "name card",
                "card": "input your json",
                "description": "description card",

            }
        }


class TokenCard(Card):
    uid: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

    class Config:
        schema_extra = {
            "uid": "generate token uid",
            "date": "12/01/2022",
            "time": "12:00:00",
        }


class UpdateCard(BaseModel):
    name: str
    card: Optional[str] = None
    description: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "name card",
                "card": "card flex message or carousel",
                "description": "description flex message or carousel",
            }
        }

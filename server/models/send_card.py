from db import PyObjectId
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field


class SendCard(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    access_token: str
    user_id: str
    default_card: Optional[bool] = False
    id_card: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "access_token": "access token long live",
                "user_id": "line name",
                "default_card": "False",
                "id_card": "id card",
            }
        }


class TokenSendCard(SendCard):
    uid: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

    class Config:
        schema_extra = {
            "uid": "generate token uid",
            "date": "12/01/2022",
            "time": "12:00:00",
        }


class QueryCard(TokenSendCard):
    name: str
    card: Optional[str] = None
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "name": "name card",
            "card": "your card",
            "description": "description card",
        }

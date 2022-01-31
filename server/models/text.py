from db import PyObjectId
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field


class TextSend(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    access_token: str
    user_id: str
    message: str

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "access_token": "access token long live",
                "user_id": "line name",
                "message": "send message",
            }
        }


class TokenTextSend(TextSend):
    uid: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

    class Config:
        schema_extra = {
            "uid": "generate token uid",
            "date": "12/01/2022",
            "time": "12:00:00",
        }

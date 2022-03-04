from db import PyObjectId
from bson import ObjectId
from typing import Optional, Dict
from pydantic import BaseModel, Field, constr


class Permission(BaseModel):
    uid: str
    username: str
    role: Optional[str] = None
    email: str
    hashed_password: str
    full_name: Optional[str] = None
    img_path: Optional[str] = None
    date: str
    time: str
    disabled: Optional[bool] = None
    _data: Optional[dict] = None


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    data: Optional[Permission] = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {"data": {}}


class Register(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    email: str
    password: Optional[constr(min_length=6)]

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                'email': 'wera.watcharapon@gmail.com',
                'password': 'secret'
            }
        }


class TokenUser(Register):
    uid: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

    class Config:
        schema_extra = {
            "uid": "uid authentication",
            "date": "12/01/2022",
            "time": "12:00:00",
        }

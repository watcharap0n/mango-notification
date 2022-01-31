from db import PyObjectId
from bson import ObjectId
from typing import Optional, Dict
from pydantic import BaseModel, Field, constr


class User(BaseModel):
    iss: str
    name: Optional[str] = None
    picture: Optional[str] = None
    aud: Optional[str] = None
    auth_time: Optional[int] = None
    user_id: Optional[str] = None
    sub: Optional[str] = None
    iat: Optional[int] = None
    exp: Optional[int] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = False
    firebase: Optional[dict] = {}
    uid: str

    class Config:
        schema_extra = {
            "example": {
                "iss": "https://session.firebase.google.com/example",
                "name": "kaneAI",
                "picture": "https://example.com/static/uploads/example.jpg",
                "aud": "auth-example",
                "auth_time": 1643273200,
                "user_id": "user_id_example",
                "sub": "sub_example",
                "iat": 1643273201,
                "exp": 1643275001,
                "email": "wera.watcharapon@gmail.com",
                "email_verified": True,
                "firebase": {},
                "uid": "example_uid"
            }
        }


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

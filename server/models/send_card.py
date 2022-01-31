from db import PyObjectId
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, HttpUrl


class DefaultCard(BaseModel):
    header: Optional[str] = None
    image: Optional[bool] = False
    path_image: Optional[HttpUrl] = None
    footer: Optional[bool] = False
    body_key: Optional[list] = ['input your key flex msg']
    body_value: Optional[list] = ['input your value flex msg'],
    name_btn: Optional[str] = 'URL',
    url_btn: Optional[str] = 'https://linecorp.com'

    class Config:
        schema_extra = {
            "example": {
                "header": "header card",
                "image": False,
                "path_image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
                "footer": False,
                "body_key": ['name', 'company'],
                "body_value": ['watcharapon', 'mango consultant'],
                "name_btn": "URL",
                "url_btn": "https://mangoserverbot.herokuapp.com"
            }
        }


class SendCard(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    access_token: str
    user_id: str
    default_card: Optional[bool] = False
    config_default_card: Optional[DefaultCard] = {
        "header": "header card",
        "image": False,
        "path_image": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        "footer": False,
        "body_key": ['name', 'company'],
        "body_value": ['watcharapon', 'mango consultant'],
        "name_btn": "URL",
        "url_btn": "https://mangoserverbot.herokuapp.com"
    }
    id_card: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "access_token": "access token long live",
                "user_id": "line name",
                "default_card": False,
                "id_card": "id card",
            }
        }


class QueryCard(SendCard):
    uid: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    name: str
    content: Optional[str] = None
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "uid": "generate token uid",
            "date": "12/01/2022",
            "time": "12:00:00",
            "name": "name card",
            "content": "your card",
            "description": "description card",
        }

from db import db
from typing import List
from models.oauth2 import User
from oauth2 import get_current_active
from starlette.responses import JSONResponse
from models.card import Card, UpdateCard, TokenCard
from models.send_card import SendCard, TokenSendCard, QueryCard
from models.text import SendText, TokenSendText
from modules.item_static import item_user
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder

router = APIRouter()

collection = "api_card"


async def check_card_duplicate(
        card: Card,
        current_user: User = Depends(get_current_active)
):
    items = await db.find(
        collection=collection, query={"uid": current_user.uid}
    )
    items = list(items)
    for item in items:
        if item["name"] == card.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="item name duplicate"
            )
    return card


async def check_access_token(payload: SendCard,
                             current_user: User = Depends(get_current_active)):
    try:
        line_bot_api = LineBotApi(payload.access_token)
        line_bot_api.get_bot_info()
        return payload
    except LineBotApiError as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.message)


async def check_card_default(payload: SendCard = Depends(check_access_token),
                             current_user: User = Depends(get_current_active)):
    if not payload.default_card:
        items = await db.find(
            collection=collection, query={"uid": current_user.uid}
        )
        items = list(items)

        for item in items:
            if item["_id"] == payload.id_card:
                item_model = jsonable_encoder(payload)
                item_model = item_user(data=item_model)
                item_model = TokenSendCard(**item_model)
                item_model = jsonable_encoder(item_model)
                item_model["name"] = item["name"]
                item_model["description"] = item["description"]
                item_model["card"] = item["card"]
                item_store = QueryCard(**item_model)
                return item_store

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"id card not found"
            )
    default_card = {
        'name': 'default card',
        'card': 'json card',
        'description': 'description card'
    }
    item_model = jsonable_encoder(payload)
    item_model = item_user(data=item_model)
    item_model = TokenSendCard(**item_model)
    item_model = jsonable_encoder(item_model)
    item_model["name"] = default_card["name"]
    item_model["card"] = default_card["card"]
    item_model["description"] = default_card["description"]
    return item_model


@router.get(
    "/", tags=["Card"], response_model=List[TokenCard],
)
async def get_card(
        current_user: User = Depends(get_current_active)
):
    """
        APIs Document เหล่านี้เป็นการสร้าง flex message หรือ carousel เองได้ เพื่อนำส่งไปยัง /api/line/card ตัวแจ้งเตือนไลน์
        สามารถเข้าไปสร้างได้ที่นี้ -> "https://developers.line.biz/flex-simulator/

    :param current_user: \n
    :return:
    """
    items = await db.find(collection=collection, query={"uid": current_user.uid})
    items = list(items)
    return items


@router.post(
    "/create", response_model=TokenCard,
    tags=["Card"],
    response_description='Integrated model',
)
async def create_card(
        card: Card = Depends(check_card_duplicate),
        current_user: User = Depends(get_current_active)
):
    """

        APIs Document เหล่านี้เป็นการสร้าง flex message หรือ carousel เองได้ เพื่อนำส่งไปยัง /api/line/card ตัวแจ้งเตือนไลน์
        สามารถเข้าไปสร้างได้ที่นี้ -> "https://developers.line.biz/flex-simulator/


    :param card \n
    :param current_user \n
    :return:
    """
    item_model = jsonable_encoder(card)
    item_model = item_user(data=item_model, current_user=current_user)
    await db.insert_one(collection=collection, data=item_model)
    item_store = TokenCard(**item_model)
    return item_store


@router.put("/query/update/{id}", response_model=TokenCard, tags=["Card"])
async def update_query_card(
        id: str,
        payload: UpdateCard,
        current_user: User = Depends(get_current_active)
):
    """

        APIs Document เหล่านี้เป็นการสร้าง flex message หรือ carousel เองได้ เพื่อนำส่งไปยัง /api/line/card ตัวแจ้งเตือนไลน์
        สามารถเข้าไปสร้างได้ที่นี้ -> "https://developers.line.biz/flex-simulator/

    :param id: \n
    :param payload: \n
    :param current_user: \n
    :return:
    """
    data = jsonable_encoder(payload)
    query = {"_id": id}
    values = {"$set": data}

    if (await db.update_one(collection=collection, query=query, values=values)) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"card not found {id}"
        )
    return payload


@router.delete("/query/delete/{id}", response_model=Card, tags=["Card"])
async def delete_query_card(
        id: str,
        current_user: User = Depends(get_current_active)
):
    """

        APIs Document เหล่านี้เป็นการสร้าง flex message หรือ carousel เองได้ เพื่อนำส่งไปยัง /api/line/card ตัวแจ้งเตือนไลน์
        สามารถเข้าไปสร้างได้ที่นี้ -> "https://developers.line.biz/flex-simulator/

    :param id: \n
    :param current_user: \n
    :return:
    """
    if (await db.delete_one(collection=collection, query={"_id": id})) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"card not found {id}"
        )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/card", response_model=QueryCard, tags=["Notify Card"])
async def send_card(
        payload: QueryCard = Depends(check_card_default),
):
    return payload


@router.post("/text", response_model=TokenSendText, tags=["Notify Text"])
async def send_text(
        payload: SendText,
        current_user: User = Depends(get_current_active)
):
    try:
        line_bot_api = LineBotApi(payload.access_token)
        line_bot_api.get_bot_info()
        item_model = jsonable_encoder(payload)
        item_model = item_user(data=item_model)
        item_store = TokenSendText(**item_model)
        return item_store
    except LineBotApiError as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.message)

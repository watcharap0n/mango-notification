from db import db
from typing import List
from models.oauth2 import User
from oauth2 import get_current_active
from starlette.responses import JSONResponse
from models.card import Card, UpdateCard, TokenCard
from models.send_card import SendCard, TokenSendCard, QueryCard
from models.text import SendText, TokenSendText
from modules.item_static import item_user
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder

router = APIRouter()

collection = "api_card"


async def check_card_duplicate(
        flex: Card,
        current_user: User = Depends(get_current_active)
):
    items = await db.find(
        collection=collection, query={"uid": current_user.uid}
    )
    items = list(items)
    for item in items:
        if item["name"] == flex.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="item name duplicate"
            )
    return flex


async def check_card_default(payload: SendCard, current_user: User = Depends(get_current_active)):
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


@router.get("/", tags=["LINE FLEX MESSAGE"], response_model=List[TokenCard])
async def get_flex(
        current_user: User = Depends(get_current_active)
):
    print(current_user.dict())
    items = await db.find(collection=collection, query={"uid": current_user.uid})
    items = list(items)
    return items


@router.post("/create", response_model=TokenCard, tags=["LINE FLEX MESSAGE"])
async def create_flex(
        flex: Card = Depends(check_card_duplicate),
        current_user: User = Depends(get_current_active)
):
    item_model = jsonable_encoder(flex)
    item_model = item_user(data=item_model, current_user=current_user)
    await db.insert_one(collection=collection, data=item_model)
    item_store = TokenCard(**item_model)
    return item_store


@router.put("/query/update/{id}", response_model=TokenCard, tags=["LINE FLEX MESSAGE"])
async def update_query_flex(
        id: str,
        payload: UpdateCard,
        current_user: User = Depends(get_current_active)
):
    data = jsonable_encoder(payload)
    query = {"_id": id}
    values = {"$set": data}

    if (await db.update_one(collection=collection, query=query, values=values)) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Flex not found {id}"
        )
    return payload


@router.delete("/query/delete/{id}", response_model=Card, tags=["LINE FLEX MESSAGE"])
async def delete_query_flex(
        id: str,
        current_user: User = Depends(get_current_active)
):
    if (await db.delete_one(collection=collection, query={"_id": id})) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Flex not found {id}"
        )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/card", response_model=QueryCard, tags=["LINE SEND FLEX MESSAGE"])
async def send_flex(
        payload: QueryCard = Depends(check_card_default),
):
    return payload


@router.post("/text", response_model=TokenSendText, tags=["LINE SEND TEXT"])
async def send_text(
        payload: SendText,
        current_user: User = Depends(get_current_active)
):
    item_model = jsonable_encoder(payload)
    item_model = item_user(data=item_model)
    item_store = TokenSendText(**item_model)
    return item_store

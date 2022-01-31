import json
from typing import Optional
from models.oauth2 import User
from oauth2 import get_current_active
from fastapi import APIRouter, Body, Depends

router = APIRouter()

NOT_CONTENT = {'detail': 'Not object'}


@router.post('/plain_obj')
async def plain_obj(payload: Optional[dict] = Body(NOT_CONTENT),
                    cuurent_user: User = Depends(get_current_active)):
    return json.dumps(payload)

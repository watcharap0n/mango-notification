import json
from typing import Optional
from linebot.models import FlexSendMessage


def content_card(
        contents: str,
        name: Optional[str] = 'Notification Mango!'
):
    contents = json.loads(contents)
    flex_msg = FlexSendMessage(
        alt_text=name,
        contents=contents)
    return flex_msg

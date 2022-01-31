import json
from typing import Optional, List
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


def config_card(
        path_image: str,
        header: str,
        body_key: list,
        body_value: list,
        name_btn: str,
        url: str
) -> dict:
    contents = []
    for k, v in zip(body_key, body_value):
        body = {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": 'input your key',
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 3
                },
                {
                    "type": "text",
                    "text": 'input your value',
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                }
            ]
        }
        body['contents'][0]['text'] = k
        body['contents'][1]['text'] = v
        contents.append(body)

    card = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": path_image,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": header,
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": contents
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": name_btn,
                        "uri": url
                    }
                }
            ],
            "flex": 0
        }
    }
    return card


def content_card_dynamic(
        name: Optional[str] = 'Notification Mango!',
        header: Optional[str] = 'Mango Notify!',
        image: Optional[bool] = False,
        path_image: Optional[str] = 'https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png',
        footer: Optional[bool] = False,
        body_key: Optional[list] = ['input your key flex msg'],
        body_value: Optional[list] = ['input your value flex msg'],
        name_btn: Optional[str] = 'URL',
        url_btn: Optional[str] = 'https://linecorp.com'
):
    contents = config_card(
        path_image=path_image,
        header=header,
        body_key=body_key,
        body_value=body_value,
        name_btn=name_btn,
        url=url_btn
    )
    contents.pop('hero', None) if not image else None
    contents.pop('footer', None) if not footer else None

    flex_msg = FlexSendMessage(
        alt_text=name,
        contents=contents
    )
    return flex_msg, contents

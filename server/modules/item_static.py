import logging
from typing import Optional
from datetime import datetime
from uuid import uuid4


def item_user(data: dict, url: Optional[bool] = False):
    """

    :param change_id:
    :param data:
    :param uuid4:
    :return:
    """

    try:
        _d = datetime.now()
        data["uid"] = uuid4().hex
        data["date"] = _d.strftime("%d/%m/%y")
        data["time"] = _d.strftime("%H:%M:%S")
        if url:
            data[
                "url"
            ] = f"https://mangoserverbot.herokuapp.com/callback/{data['token']}"
        return data
    except KeyError:
        raise logging.exception("your key error")
    except Exception:
        raise logging.exception("something error")

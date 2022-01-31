"""
database and authentication master
    - mongodb
    - firebase realtime
    - firebase admin (authentication)

"""

import os
from .database import MongoDB
from .object_str import CutId, PyObjectId


client = os.environ['MONGODB_URI']
db = MongoDB(database_name='MangoBOT', uri=client)


def generate_token(engine):
    """

    :param engine:
    :return:
    """
    obj = CutId(_id=engine)
    Id = obj.dict()['id']
    return Id

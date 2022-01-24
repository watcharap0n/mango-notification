from firebase_admin import credentials
import firebase_admin
from typing import Optional
import pyrebase


class ConfigFirebase:
    def __init__(self, path_db: Optional[str] = None, path_auth: Optional[str] = None):
        self.path_db = path_db
        self.path_auth = credentials.Certificate(path_auth)
        firebase_admin.initialize_app(self.path_auth)

    def authentication(self):
        firebase = self.path_db
        pb = pyrebase.initialize_app(firebase).auth()

        return pb

    def firebase_realtime(self):
        firebase = self.path_db
        config = pyrebase.initialize_app(firebase)
        db = config.database()
        return db

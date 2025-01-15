# database/db.py
from pymongo import MongoClient
from config import Config

class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client[Config.DB_NAME]
        self.users = self.db.users
        self.responses = self.db.responses
        self.pairs = self.db.pairs

    def close(self):
        self.client.close()
from motor import motor_asyncio as motor
import pprint
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_ADDRESS = os.getenv('MONGO_ADDRESS')
MONGO_STRING = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_ADDRESS}/?retryWrites=true&w=majority"

class Database:
    def __init__(self):
        self.client = motor.AsyncIOMotorClient(MONGO_STRING)

    def close(self):
        self.client.close()

mongo_database = Database()
        
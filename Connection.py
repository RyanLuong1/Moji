from pymongo import MongoClient
from dotenv import load_dotenv
import os
mongo_url = os.getenv('CONNECTION_URL')

class Connect(object):
    @staticmethod
    def get_connect():
        return MongoClient(mongo_url)
from pymongo import MongoClient
from bson import ObjectId
from decouple import config


client = MongoClient(config('MONGO_URI'))
db = client.get_default_database()


def get_database():
    return db


def get_collection(collection_name):
    return db[collection_name]


def to_object_id(id):
    return ObjectId(id)

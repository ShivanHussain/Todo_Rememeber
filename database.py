import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

# Explicitly select database
db = client["Todo_Remember"]

tasks_collection = db["tasks"]

def init_db():
    tasks_collection.create_index("status")

def get_db():
    return db

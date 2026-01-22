import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.get_database()  # Automatically picks 'task' from URI
tasks_collection = db["tasks"]

def init_db():
    """Optional: create indexes for faster queries"""
    tasks_collection.create_index("status")

def get_db():
    return db

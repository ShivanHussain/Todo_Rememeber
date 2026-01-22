from database import tasks_collection
from bson import ObjectId

def create_task(task_data: dict):
    """Insert a new task"""
    result = tasks_collection.insert_one(task_data)
    return str(result.inserted_id)

def get_all_tasks():
    """Return all tasks"""
    return list(tasks_collection.find())

def get_task_by_id(task_id):
    try:
        return tasks_collection.find_one({"_id": ObjectId(task_id)})
    except:
        return None

def update_task(task_id, update_data: dict):
    try:
        result = tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )
        return result.modified_count
    except:
        return 0

def delete_task(task_id):
    try:
        result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count
    except:
        return 0

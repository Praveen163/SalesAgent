from pymongo import MongoClient
import json
from agents import  function_tool

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["LPU"]
collection = db["courses"]

@function_tool
def run_mongo_command(command_type: str, command: list):
    """
    Executes a MongoDB command: either find or aggregate.

    Args:
        command_type (str): 'find' or 'aggregate'.
        command (dict or list): MongoDB query.

    Returns:
        list or dict: Query results.
    """
    try:
        print("Database called\n",command_type,"\n","Command : \n", command)
        if command_type == "find":
            query = command.get("query", {})
            projection = command.get("projection", None)
            result = collection.find(query, projection)
            fresult = list(result)
            print("\n \n Results : \n",fresult)
            return fresult

        elif command_type == "aggregate":
            result = collection.aggregate(command)
            fresult = list(result)
            print("\n \n Results : \n",fresult)
            return fresult

        else:
            print("error")
            return {"error": "Unsupported command type"}
    except Exception as e:
        print("error :: ",e)
        return {"error": str(e)}



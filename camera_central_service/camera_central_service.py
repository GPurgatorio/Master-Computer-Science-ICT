from pymongo import MongoClient
import json

from config import DB_URL

mongo_client = MongoClient(DB_URL)
db = mongo_client.db

# TODO 
def handle_request(request):
    can_access = False
    username = ""
    # # Get id user associated to the encoded face
    # user = db.users.find_one({"face_code": request["encoding"]})
    # if user and request["door_id"] in user["rooms"]:
    #     username = user["username"]
    #     # If a 2-factor authentication is required
    #     policy = db.policies.find_one({"user_id": user["_id"], "room_id": request["door_id"]})
    #     if policy and policy["type"]==1:
    #         # TODO
    #         can_access = check_bluetooth_device(user)
    #     # Otherwise
    #     else:
    #         can_access = True
    
    response = json.dumps({
        "door_id": request["door_id"],
        "user": username,
        "open": can_access
    })
    return response

def check_bluetooth_device(user):
    return True
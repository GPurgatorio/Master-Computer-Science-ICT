from pymongo import MongoClient
import json

from config import DB_URL

mongo_client = MongoClient(DB_URL)
db = mongo_client.chessaRMI

def handle_request(request):
    response = {
        "door_id": "",
        "user": "",
        "open": False
    }

    try:        
        # Check if the user exists
        user = db.users.find_one({"face_code": {"$all": request["encoding"]}})
        if not user:
            return json.dumps(response)
        response["user"] = user["email"]

        # Check if the room exists
        room = db.rooms.find_one({"name": request["door_id"]})
        if not room:
            return json.dumps(response)
        response["door_id"] = room["name"]

        # Check access rights
        if room["_id"] in user["rooms"]:
            # If a 2-factor authentication is required
            policy = db.policies.find_one({"user_id": user["_id"], "room_id": request["door_id"]})
            if policy and policy["type"]==1:
                response["open"] = check_bluetooth_device(user)
            # Otherwise
            else:
                response["open"] = True
    except Exception as e:
        print(e)

    return json.dumps(response)

# TODO
def check_bluetooth_device(user):
    return True
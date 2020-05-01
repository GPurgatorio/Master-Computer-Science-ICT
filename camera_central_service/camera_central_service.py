import json
from datetime import datetime, timedelta

from pymongo import MongoClient

from config import DB_URL, EXPIRATION_DATE_FORMAT, BT_TIME_DELTA

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
            policy = db.policies.find_one({"user_id": user["_id"], "room_id": room["_id"]})
            if policy:
                if policy["type"] == 1:
                    response["open"] = check_bluetooth_device(user, room)
                else:
                    response["open"] = True
            else:
                response["open"] = False
    except Exception as e:
        print(e)

    return json.dumps(response)


def check_bluetooth_device(user, room):

    user_devices = user["devices"]
    valid_expiration_date = datetime.strftime(
        datetime.now() - timedelta(seconds=BT_TIME_DELTA*2), EXPIRATION_DATE_FORMAT)

    valid_devices = db.discovered_devices.find(
        {"door_id": room['name'],
         "expiration_date": {"$gte": valid_expiration_date}}).sort("expiration_date").limit(1)

    # no recent devices discovered
    if not valid_devices.count():
        return False
    else:
        # check if one of the devices belongs to 'user'
        return any(d in user_devices for d in valid_devices[0]['devices'])

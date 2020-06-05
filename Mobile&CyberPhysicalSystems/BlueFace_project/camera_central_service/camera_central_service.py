import face_recognition
import json
from datetime import datetime, timedelta
from numpy import array
from pymongo import MongoClient

from config import DB_URL, EXPIRATION_DATE_FORMAT, BT_TIME_DELTA, TOLERANCE


mongo_client = MongoClient(DB_URL)
db = mongo_client.chessaRMI


def handle_request(request):
    response = {
        "door_id": "",
        "user": "",
        "open": False
    }

    try:
        # Check if the room exists
        room = db.rooms.find_one({"name": request["door_id"]})
        if not room:
            return None, None
        response["door_id"] = room["name"]

         # Check if the user exists
        user = None
        enc = array(request["encoding"])
        for usr in db.users.find():
            if face_recognition.compare_faces([array(usr["face_code"])], enc, tolerance=TOLERANCE)[0]:
                user = usr
                break
        if not user:
            return room["name"], json.dumps(response)
        response["user"] = user["email"]

        # Check access rights
        policy = db.policies.find_one({"user_id": user["_id"], "room_id": room["_id"]})
        if policy:
            # If a 2-factor authentication is required
            if policy["type"] == 1:
                response["open"] = check_bluetooth_device(user, room)
            else:
                response["open"] = True
    except Exception as e:
        print("ERROR: "+str(e))

    return room["name"], json.dumps(response)


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

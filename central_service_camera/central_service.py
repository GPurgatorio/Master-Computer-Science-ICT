#TODO: Integrate to the central service

''' The expected request payload is a JSON string with the following format:
        {
            "door_id": string,
            "encoding": array
        }
    where "door_id" is the identifier associated with the door and "encoding" is the 128-dimensional 
    encoding of the face of the user who tries to access the room.

    The replies to the requests will be published on the topic RESPONSE_TOPIC, specified in the config.py 
    file and their payload will be a JSON string with the following format:
        {
            "door_id": string,
            "user": string,
            "open": Bool
        }
    where "door_id" is the identifier of the door in the request, "user" is the username associated with
    the encoded face in the request and "open" is True only if the user has the rights to access the room.
'''

import paho.mqtt.client as mqtt
import json
from config import *


# TODO 
def handle_request(data):
    response = json.dumps({
        "door_id": data["door_id"],
        "user": "boh",
        "open": True
    })
    print(response)
    return response


def on_connect(mqtt_client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_subscribe(mqtt_client, userdata, mid, granted_qos):
    print("Subscribe ok")

def on_message(mqtt_client, userdata, message):
    print("Message received")
    payload = message.payload.decode()
    reply = handle_request(json.loads(payload))
    mqtt_client.publish(topic=RESPONSE_TOPIC, payload=reply)

def on_publish(mqtt_client, userdata, mid):
    print("Message published")

def run():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_publish = on_publish
    mqtt_client.on_message = on_message
    mqtt_client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)

    mqtt_client.connect(MQTT_ADDRESS, port=MQTT_PORT)
    mqtt_client.subscribe(REQUEST_TOPIC)

    mqtt_client.loop_forever()


if __name__ == "__main__":
    run()

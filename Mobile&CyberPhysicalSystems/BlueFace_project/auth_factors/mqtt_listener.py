from pymongo import MongoClient
from config import *

import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
mongo = MongoClient(DB_URL)
db = mongo["chessaRMI"]


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    if msg.topic == BT_DISCOVER_TOPIC:
        payload = json.loads(msg.payload)
        db["discovered_devices"].insert_one(payload)
        print("Added {} discovered devices from room {}, with expiration date: {}".
              format(len(payload['devices']), payload['door_id'], payload['expiration_date']))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def init_mqtt():
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    client.username_pw_set(username=MQTT_ID, password=MQTT_PASS)
    client.connect(MQTT_SERVER, MQTT_PORT, MQTT_WAIT_TIME)

    (result, mid) = client.subscribe(BT_DISCOVER_TOPIC, 0)


if __name__ == "__main__":
    init_mqtt()
    client.loop_forever()


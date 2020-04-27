import json
import logging
import sys
from datetime import datetime, timedelta
from threading import Event

import paho.mqtt.client as mqtt

from config import *
from mcps_bluetooth import discover_devices

client = mqtt.Client()
ticker = Event()
logger = logging.getLogger()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_publish(client, userdata, mid):
    print("Message published")
    pass


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def init_mqtt():
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe

    client.username_pw_set(username=MQTT_ID, password=MQTT_PASS)
    client.connect(MQTT_SERVER, MQTT_PORT, MQTT_WAIT_TIME)

    (result, mid) = client.subscribe(BT_DISCOVER_TOPIC, 0)
    # if result == mqtt.MQTT_ERR_NO_CONN:
    #    print("Not connected to the broker")
    print("Succesfully connected to the broker.")


def _get_expiration_time():
    expiration_date = datetime.now() + timedelta(seconds=BT_TIME_DELTA)
    return datetime.strftime(expiration_date, EXPIRATION_DATE_FORMAT)


def loop_discover():
    # try-catch needed because sometimes bluetooth modules goes in segmentation fault.
    try:
        devices = discover_devices()
    except Exception:
        devices = []

    payload = json.dumps({
        "door_id": DOOR_ID,
        "devices": str(devices),
        "expiration_time": _get_expiration_time()
    })
    print(payload)
    client.publish(topic=BT_DISCOVER_TOPIC, payload=payload)


if __name__ == "__main__":
    init_mqtt()
    while not ticker.wait(BT_TIME_DELTA+1):
        loop_discover()


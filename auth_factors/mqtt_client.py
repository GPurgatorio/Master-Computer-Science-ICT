import json
from datetime import datetime, timedelta
from threading import Event

import paho.mqtt.client as mqtt

from config import *
from mcps_bluetooth import discover_devices

client = mqtt.Client()
ticker = Event()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_publish(client, userdata, mid):
    pass


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def init_mqtt():
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe

    client.username_pw_set(username=MQTT_ID, password=MQTT_PASS)
    client.connect(MQTT_SERVER, MQTT_PORT, MQTT_WAIT_TIME)
    client.loop_start()


def _get_expiration_time():
    expiration_date = datetime.now() + timedelta(seconds=BT_TIME_DELTA)
    return datetime.strftime(expiration_date, EXPIRATION_DATE_FORMAT)


def loop_discover():
    try:
        devices = discover_devices()
    except Exception as e:
        print(e)
        devices = []

    payload = json.dumps({
        "door_id": DOOR_ID,
        "devices": devices,
        "expiration_time": _get_expiration_time()
    })

    client.publish(topic=BT_DISCOVER_TOPIC, payload=payload)


if __name__ == "__main__":
    init_mqtt()
    try:
        while not ticker.wait(BT_TIME_DELTA + 1):
            loop_discover()
    finally:
        client.loop_stop()

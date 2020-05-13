''' The requests will be published on the topic REQUEST_TOPIC, specified in the config.py file. 
    The requests payload will be a JSON string with the following format:
        {
            "door_id": string,
            "encoding": array
        }
    where "door_id" is the identifier associated with the door and "encoding" is the 
    128-dimensional encoding of the face of the user who tries to open the door.
'''

import paho.mqtt.client as mqtt
import json
from config import MQTT_ADDRESS, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, REQUEST_TOPIC


mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("Message published")

def init_mqtt():
    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish
    mqtt_client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
    
    mqtt_client.connect(MQTT_ADDRESS, port=MQTT_PORT)
    mqtt_client.subscribe(REQUEST_TOPIC)
    mqtt_client.loop_start()

def send_request(face_encoding, door_id):
    request = json.dumps({
        "door_id": door_id,
        "encoding": face_encoding.tolist()
    })
    mqtt_client.publish(topic=REQUEST_TOPIC, payload=request)

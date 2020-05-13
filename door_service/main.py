import paho.mqtt.client as mqtt
from services import door_services
from config import MQTT_ID, MQTT_PASS, MQTT_SERVER, DOOR_MESSAGE_RESPONSE


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(DOOR_MESSAGE_RESPONSE, 0)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = str(msg.payload, 'utf-8')
    topic = str(msg.topic)
    print(topic + " " + payload)
    if topic == DOOR_MESSAGE_RESPONSE:
        try:
            door_services.open_door_message_handler(payload)
        except Exception as e:
            print(e)


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.username_pw_set(username=MQTT_ID, password=MQTT_PASS)
client.connect(MQTT_SERVER, 8883, 10)

try:
    client.loop_forever()
finally:
    door_services.cleanup_handler()

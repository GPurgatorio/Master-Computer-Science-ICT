MQTT_ADDRESS = "raspberrypigio2.zapto.org"
MQTT_PORT = 8883
MQTT_USERNAME = "giobart"
MQTT_PASSWORD = "qwerty99" # Ciste Approves ;)

REQUEST_TOPIC = "door/request"

DOOR_ID = "door123"
FDT = 30 # Frames to discard if nothing is detected
FDT_FACE = 60 # Frames to discard after detecting a face
FDT_AFTER_REQUEST = 150 # Frames to discard after sending a request

TOLERANCE = 0.4 # tolerance for face_recognition.compare_faces()
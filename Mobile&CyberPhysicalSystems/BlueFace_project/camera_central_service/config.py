MQTT_ADDRESS = "raspberrypigio2.zapto.org"
MQTT_PORT = 8883
MQTT_USERNAME = "giobart"
MQTT_PASSWORD = "qwerty99"

DB_PASSWORD = "chessarmi"
DB_URL = "mongodb+srv://chessarmi:"+DB_PASSWORD + \
	"@mcps-project-txguh.mongodb.net/chessaRMI?retryWrites=true&w=majority"

REQUEST_TOPIC = "door/request"
RESPONSE_TOPIC = "door/"

EXPIRATION_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
BT_TIME_DELTA = 5

TOLERANCE = 0.4 # tolerance for face_recognition.compare_faces()

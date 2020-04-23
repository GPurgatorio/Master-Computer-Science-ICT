import face_recognition
import cv2
import json
from time import time, sleep

from config import DOOR_ID, WAIT_TIME_FACE, WAIT_TIME_REQUEST
import mqtt_client


def run_camera():
    mqtt_client.connect()

    video_capture = cv2.VideoCapture(0)
    if not video_capture:
        print("Error with camera")
        return

    prev_enc = []
    prev_enc_time = 0
    while True:
        # Check if the webcam detects a face
        ret, frame = video_capture.read()
        enc = get_face_encoding(frame)

        # If there is a detected face and it is equal to the one detected before
        if len(enc)!=0 and len(prev_enc)!=0 and face_recognition.compare_faces([prev_enc], enc)[0]:
            # Send the request only when WAIT_TIME_FACE is elapsed
            if time() - prev_enc_time > WAIT_TIME_FACE:
                mqtt_client.send_request(enc, DOOR_ID)
                prev_enc = []
                sleep(WAIT_TIME_REQUEST)
        # Otherwise, update detected face
        else:
            prev_enc = enc
            if len(enc) != 0:
                prev_enc_time = time()
                
def get_face_encoding(frame):
    # Get faces location
    face_locations = face_recognition.face_locations(frame)
    # Encode only if the frame contains one and only one face
    if len(face_locations) == 1:
        return face_recognition.face_encodings(frame, face_locations)[0]
    else:
        return []


if __name__ == '__main__':
    run_camera()

import face_recognition
import cv2
import json
from time import time

from config import DOOR_ID, FDT, FDT_FACE, FDT_AFTER_REQUEST, TOLERANCE
import mqtt_client


def run_camera():
    mqtt_client.init_mqtt()

    video_capture = cv2.VideoCapture(0)
    if not video_capture:
        print("Error with camera")
        return

    while True:
        ret, frame = video_capture.read()
        #print(time())
        enc = get_face_encoding(frame)

        # If a face has been detected
        if len(enc)!=0:
            #print("face detected")
            discard_frames(video_capture, FDT_FACE)
            ret, frame = video_capture.read()
            #print(time())
            enc2 = get_face_encoding(frame)

            # If the face is still in front of the camera, send the request
            if len(enc2)!=0 and face_recognition.compare_faces([enc], enc2, tolerance=TOLERANCE)[0]:
                #print("sending request")
                mqtt_client.send_request(enc, DOOR_ID)
                discard_frames(video_capture, FDT_AFTER_REQUEST)
            #else:
                #print("not equal")

        else:
            discard_frames(video_capture, FDT)
        

                
def get_face_encoding(frame):
    # Get faces location
    face_locations = face_recognition.face_locations(frame)
    # Encode only if the frame contains one and only one face
    if len(face_locations) == 1:
        return face_recognition.face_encodings(frame, face_locations)[0]
    else:
        return []

def discard_frames(video_capture, n):
    for i in range(n):
        video_capture.read()

if __name__ == '__main__':
    run_camera()

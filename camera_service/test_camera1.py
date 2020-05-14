import face_recognition
import cv2
from time import time

from config import FDT, FDT_FACE, FDT_AFTER_REQUEST, TOLERANCE

def get_face_encoding(frame):
    # Get faces location
    face_locations = face_recognition.face_locations(frame)
    # Encode only if the frame contains one and only one face
    print(str(len(face_locations))+" faces detected")
    if len(face_locations) == 1:
        return face_recognition.face_encodings(frame, face_locations)[0]
    else:
        return []

def discard_frames(video_capture, n):
    for i in range(n):
        video_capture.read()

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    print(time())
    enc = get_face_encoding(frame)
    #print(enc)

    # If a face has been detected
    if len(enc)!=0:
        print("face detected")
        discard_frames(video_capture, FDT_FACE)
        ret, frame = video_capture.read()
        print(time())

        # Check if the face is still in front of the camera
        enc2 = get_face_encoding(frame)
        if len(enc2)!=0 and face_recognition.compare_faces([enc], enc2, tolerance=TOLERANCE)[0]:
            print("sending request")
            discard_frames(video_capture, FDT_AFTER_REQUEST)
        else:
            print("not equal")

    discard_frames(video_capture, FDT)
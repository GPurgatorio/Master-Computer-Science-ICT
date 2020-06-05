import json
import face_recognition

picture_of_me = face_recognition.load_image_file("./faces/lenna.png")
my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

print(my_face_encoding.tolist())
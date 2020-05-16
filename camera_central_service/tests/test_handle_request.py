import unittest
import face_recognition
import json

from camera_central_service import handle_request

UNK_image = "faces/UNK.jpeg"
AB_image = "faces/AB.jpg"

class TestAccessRoom(unittest.TestCase):

    # An user tries to access a non-existing room
    def test_access_unknown_room(self):
        encoding = get_encoding(AB_image)
        request = {
            "door_id": "non-existing_room",
            "encoding": encoding
        }
        id_door, data = handle_request(request)

        self.assertIsNone(id_door)
        self.assertIsNone(data)

    # An unknown user tries to access room_A
    def test_access_unknown_user(self):
        encoding = get_encoding(UNK_image)
        request = {
            "door_id": "room_A",
            "encoding": encoding
        }
        id_door, data = handle_request(request)
        reply = json.loads(data)
        
        assert reply["user"]==""
        self.assertFalse(reply["open"])
        
    # User A B access room_storage (without 2-factor authentication)
    def test_access_success(self):
        encoding = get_encoding(AB_image)
        request = {
            "door_id": "room_storage",
            "encoding": encoding
        }
        id_door, data = handle_request(request)
        reply = json.loads(data)

        assert reply["user"]=="a@a.com"
        assert reply["door_id"]=="room_storage"
        self.assertTrue(reply["open"])
    
    # User A B cannot access room_C
    def test_access_fail(self):
        encoding = get_encoding(AB_image)
        request = {
            "door_id": "room_C",
            "encoding": encoding
        }
        id_door, data = handle_request(request)
        reply = json.loads(data)

        assert reply["user"]=="a@a.com"
        assert reply["door_id"]=="room_C"
        self.assertFalse(reply["open"])


def get_encoding(input_image):
    picture = face_recognition.load_image_file(input_image)
    encoding = face_recognition.face_encodings(picture)[0]
    return encoding.tolist()


if __name__ == '__main__':
    unittest.main()

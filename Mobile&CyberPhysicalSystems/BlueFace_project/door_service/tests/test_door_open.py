import unittest
from config import *
import json
from services.door_services import open_door_message_handler


class TestDoorOpen(unittest.TestCase):

    def test_open(self):
        door_message = {
            "to": DEVICE_ID,
            "user": "Luke Skywalker",
            "open": True
        }

        opened = open_door_message_handler(json.dumps(door_message))

        assert opened

    def test_open_error(self):
        door_message = {
            "to": DEVICE_ID,
            "user": "Luke Skywalker",
            "open": False
        }

        opened = open_door_message_handler(json.dumps(door_message))

        assert not opened

    def test_open_not_this_user(self):
        door_message = {
            "to": "random_device_id_fff9983411",
            "user": "Luke Skywalker",
            "open": False
        }

        opened = open_door_message_handler(json.dumps(door_message))

        assert not opened


if __name__ == '__main__':
    unittest.main()

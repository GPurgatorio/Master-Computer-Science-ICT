import unittest
import json
from flask import request, jsonify
from monolith.app import app as tested_app


class TestStories(unittest.TestCase):
	def testOpenStory(self):
		app = tested_app.test_client()

                # 1. Testing an existing story
                # reply = app.get('/stories/1')
                # body = json.loads(str(reply.data, 'utf8'))
                # self.assertEqual(body, 0) # ???

                # # 2. Testing a non existing story
                # reply = app.get('/stories/100')
                # body = json.loads(str(reply.data, 'utf8'))
                # self.assertEqual(body, 0) # ???
                # 3. Testing a wrong method type
                reply = app.post('/stories/1')
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(reply.status_code, 405)
                
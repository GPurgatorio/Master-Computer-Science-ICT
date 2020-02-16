import datetime

import flask_testing

from APIGateway.app import create_app
from APIGateway.urls import TEST_DB


class TestReaction(flask_testing.TestCase):
    app = None

    def create_app(self):
        global app
        app = create_app(TEST_DB)
        return app

    def test_search(self):
        # Search for an existing story
        self.client.get('http://127.0.0.1:5000/search?query=bubble')

        self.assert_template_used('search.html')
        self.assertEqual(len(self.get_context_variable('list_of_stories')), 1)
        self.assertEqual(len(self.get_context_variable('list_of_users')), 0)

        # Search for an existing story and an existing user
        self.client.get('http://127.0.0.1:5000/search?query=admin')

        self.assert_template_used('search.html')
        self.assertEqual(len(self.get_context_variable('list_of_stories')), 1)
        self.assertEqual(len(self.get_context_variable('list_of_users')), 1)

        # Search for two existing story
        self.client.get('http://127.0.0.1:5000/search?query=from')

        self.assert_template_used('search.html')
        self.assertEqual(len(self.get_context_variable('list_of_stories')), 2)
        self.assertEqual(len(self.get_context_variable('list_of_users')), 0)

        # Search for two users with same firstname
        self.client.get('http://127.0.0.1:5000/search?query=first')

        self.assert_template_used('search.html')
        self.assertEqual(len(self.get_context_variable('list_of_stories')), 0)
        self.assertEqual(len(self.get_context_variable('list_of_users')), 2)

        # Search for two users with same lastname
        self.client.get('http://127.0.0.1:5000/search?query=exe')

        self.assert_template_used('search.html')
        self.assertEqual(len(self.get_context_variable('list_of_stories')), 0)
        self.assertEqual(len(self.get_context_variable('list_of_users')), 2)

        # Search for not existing result
        self.client.get('http://127.0.0.1:5000/search?query=nowords')

        self.assert_template_used('search.html')
        self.assertEqual(len(self.get_context_variable('list_of_stories')), 0)
        self.assertEqual(len(self.get_context_variable('list_of_users')), 0)

        # Search malformed
        self.client.get('http://127.0.0.1:5000/search?=nowords')

        self.assert_template_used('search.html')
        self.assertEqual(len(self.get_context_variable('list_of_stories')), 0)
        self.assertEqual(len(self.get_context_variable('list_of_users')), 0)
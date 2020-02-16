import datetime
import json
import os
import random as rnd
import unittest

import flask_testing

from monolith.app import create_app
from monolith.classes.DiceSet import DiceSet, Die
from monolith.database import User, db
from monolith.forms import LoginForm
from monolith.urls import TEST_DB

path = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/standard/"


class TestDiceSet(unittest.TestCase):

    def test_empty_dice_set(self):
        with self.assertRaises(TypeError):
            DiceSet()

    def test_throw_and_serialize_dice_set(self):
        rnd.seed(574891)
        die1 = Die(path + "die0.txt")
        die2 = Die(path + "die1.txt")
        die3 = Die(path + "die2.txt")
        dice = [die1, die2, die3]
        dice_set = DiceSet(dice)

        # throw dice
        expected_res = ['bag', 'clock', 'bus']
        self.assertEqual(dice_set.throw_dice(), expected_res)

        # serialize set
        serialized_set = dice_set.serialize()
        expected_serialized_set = json.dumps(dice_set.pips)
        self.assertEqual(serialized_set, expected_serialized_set)


class TestTemplateDiceSet(flask_testing.TestCase):
    app = None

    # First thing called
    def create_app(self):
        global app
        app = create_app(database=TEST_DB)
        return app

    # Set up database for testing here
    def setUp(self) -> None:
        print("SET UP")
        with app.app_context():
            example = User()
            example.firstname = 'Admin'
            example.lastname = 'Admin'
            example.email = 'example@example.com'
            example.dateofbirth = datetime.datetime(2020, 10, 5)
            example.is_admin = True
            example.set_password('admin')
            db.session.add(example)

            db.session.commit()

        payload = {'email': 'example@example.com',
                   'password': 'admin'}

        form = LoginForm(data=payload)

        self.client.post('/users/login', data=form.data, follow_redirects=True)

    # Executed at end of each test
    def tearDown(self) -> None:
        print("TEAR DOWN")
        db.session.remove()
        db.drop_all()

    def test_authorization(self):
        response = self.client.post('/users/logout')

        self.assert_redirects(response, '/')

        self.assert401(self.client.get('stories/new/settings'))
        self.assert401(self.client.post('stories/new/roll'))

    def test_dice_set(self):
        # test settings template
        self.assert200(self.client.get('/stories/new/settings'))
        self.assert_template_used('settings.html')

        # test set not exist
        self.assertRedirects(
            self.client.post('/stories/new/roll',
                             data={'dice_number': 2, 'dice_img_set': 'notexist'}), '/stories/new/settings')

        # test empty set
        self.assertRedirects(
            self.client.post('/stories/new/roll',
                             data={'dice_number': 2, 'dice_img_set': 'emptyset'}), '/stories/new/settings')

        # test set not exist from same page with bad request key
        with self.client.session_transaction() as sess:
            sess['dice_number'] = 2
            sess['dice_img_set'] = 'notexist'
            self.assertRedirects(self.client.post('/stories/new/roll',
                                                  data={'dice_number': 2, 'dice_img_set': 'badrequestkey'}),
                                 '/stories/new/settings')

        # test set exist 
        self.client.post('/stories/new/roll',
                         data={'dice_number': 2, 'dice_img_set': 'halloween'})
        self.assert_template_used('roll_dice.html')

        # test set exist from same page with bad request key (BadRequestKeyError)
        with self.client.session_transaction() as sess:
            sess['dice_number'] = 2
            sess['dice_img_set'] = 'animal'
            self.client.post('/stories/new/roll')
            self.assert_template_used('roll_dice.html')

    # Tests for POST, PUT and DEL requests ( /settings )
    def test_requests_settings(self):
        self.assert405(self.client.post('stories/new/settings'))
        self.assert405(self.client.put('stories/new/settings'))
        self.assert405(self.client.delete('stories/new/settings'))

    # Tests for GET, PUT and DEL requests ( /settings )
    def test_requests_roll(self):
        self.assert405(self.client.get('stories/new/roll'))
        self.assert405(self.client.put('stories/new/roll'))
        self.assert405(self.client.delete('stories/new/roll'))

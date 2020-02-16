import datetime
import json

import flask_testing

from UsersService.app import create_app
from UsersService.database import db, User
from UsersService.urls import TEST_DB


class TestUsers(flask_testing.TestCase):
    app = None

    def create_app(self):
        global app
        app = create_app(database=TEST_DB)
        return app

    # Set up database for testing
    def setUp(self) -> None:
        with app.app_context():
            # Create two users
            user = db.session.query(User).filter(User.email == 'example@example.com').first()
            if user is None:
                example = User()
                example.firstname = 'Admin'
                example.lastname = 'Admin'
                example.email = 'example@example.com'
                example.dateofbirth = datetime.datetime(2010, 10, 5)
                example.is_admin = True
                example.set_password('admin')
                db.session.add(example)
                db.session.commit()

            user = db.session.query(User).filter(User.email == 'cantagallo@example.com').first()
            if user is None:
                example = User()
                example.firstname = 'Cantagallo'
                example.lastname = 'Rooster'
                example.email = 'cantagallo@example.com'
                example.dateofbirth = datetime.datetime(2010, 10, 10)
                example.is_admin = True
                example.set_password('p')
                db.session.add(example)
                db.session.commit()

            user = db.session.query(User).filter(User.email == 'thebest@example.com').first()
            if user is None:
                example = User()
                example.firstname = 'Cantagallo'
                example.lastname = 'TheBest'
                example.email = 'thebest@example.com'
                example.dateofbirth = datetime.datetime(2010, 10, 8)
                example.is_admin = True
                example.set_password('p')
                db.session.add(example)
                db.session.commit()

            user = db.session.query(User).filter(User.email == 'theworst@example.com').first()
            if user is None:
                example = User()
                example.firstname = 'TheWorst'
                example.lastname = 'Rooster'
                example.email = 'theworst@example.com'
                example.dateofbirth = datetime.datetime(2010, 10, 2)
                example.is_admin = True
                example.set_password('p')
                db.session.add(example)
                db.session.commit()

    # Executed at end of each test
    # Tear down database at the end of the tests

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    # Assert reply data
    def assertDescription(self, reply, expected_description):
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body['description'], expected_description)

    # ----------- Test functions -----------

    def test_all_users(self):
        reply = self.client.get('/users')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body, [
            {"email": "example@example.com", "firstname": "Admin", "id": 1, "lastname": "Admin"},
            {"email": "cantagallo@example.com", "firstname": "Cantagallo", "id": 2, "lastname": "Rooster"},
            {"email": "thebest@example.com", "firstname": "Cantagallo", "id": 3, "lastname": "TheBest"},
            {"email": "theworst@example.com", "firstname": "TheWorst", "id": 4, "lastname": "Rooster"}
        ])

    def test_create_user(self):
        # Email address already used
        data = json.dumps({
            'firstname': 'Natalia',
            'lastname': 'Prova',
            'dateofbirth': datetime.datetime(2010, 10, 5).strftime('%Y-%m-%d'),
            'email': 'cantagallo@example.com',
            'password': 'Prova'
        })
        reply = self.client.post('/users/create', data=data)
        self.assertStatus(reply, 406)

        # Date of birth > today
        data = json.dumps({
            'firstname': 'Prova',
            'lastname': 'Prova',
            'dateofbirth': datetime.datetime(2050, 10, 5).strftime('%Y-%m-%d'),
            'email': 'Prova',
            'password': 'Prova'
        })
        reply = self.client.post('/users/create', data=data)
        self.assertStatus(reply, 400)
        self.assertDescription(reply, 'Date of birth can not be greater than today')

        # Bad parameters
        data = json.dumps({
            'firstname': 'Prova',
            'dateofbirth': 'Not a date',
            'email': 'Prova',
            'password': 'Prova'
        })
        reply = self.client.post('/users/create', data=data)
        self.assertStatus(reply, 400)
        self.assertDescription(reply, 'Error with one parameter')

        # Correct request
        data = json.dumps({
            'firstname': 'Prova',
            'lastname': 'Prova',
            'dateofbirth': datetime.datetime(2010, 10, 5).strftime('%Y-%m-%d'),
            'email': 'Prova',
            'password': 'Prova'
        })
        reply = self.client.post('/users/create', data=data)
        self.assertStatus(reply, 201)
        # Check new user exists
        user = db.session.query(User).filter(User.email == 'Prova').first()
        self.assertTrue(user)

    def test_login(self):
        # Correct request
        data = json.dumps({
            'email': 'cantagallo@example.com',
            'password': 'p'
        })
        reply = self.client.post('/users/login', data=data)
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body,
                         {"email": "cantagallo@example.com", "firstname": "Cantagallo", "id": 2, "lastname": "Rooster"}
                         )

        # Password uncorrect
        data = json.dumps({
            'email': 'cantagallo@example.com',
            'password': 'wrong'
        })
        reply = self.client.post('/users/login', data=data)
        self.assertStatus(reply, 400)
        self.assertDescription(reply, 'Password uncorrect')

        # Email does not exist
        data = json.dumps({
            'email': 'wrong',
            'password': 'p'
        })
        reply = self.client.post('/users/login', data=data)
        self.assertStatus(reply, 404)

        # Bad parameters
        data = json.dumps({
            'email': 'cantagallo@example.com',
        })
        reply = self.client.post('/users/login', data=data)
        self.assertStatus(reply, 400)
        self.assertDescription(reply, 'Error with one parameter')

    def test_user_data(self):
        # Correct request
        reply = self.client.get('users/1')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body, {
            'dateofbirth': '05/10/2010', 'email': 'example@example.com',
            'firstname': 'Admin', 'follower_counter': 0, 'id': 1,
            'is_admin': True, 'lastname': 'Admin'
        })

        # User does not exist
        reply = self.client.get('users/6')
        self.assertStatus(reply, 404)

    def test_follow(self):
        # Requests with bad parameters
        reply = self.client.post('users/1/follow?current_user_id=')
        self.assertStatus(reply, 400)
        self.assertDescription(reply, 'Error with current_user_id parameter')

        reply = self.client.post('users/1/follow?current_user_id=aa')
        self.assertEqual(reply.status_code, 400)
        self.assertDescription(reply, 'Error with current_user_id parameter')

        # The user to follow does not exist
        reply = self.client.post('users/6/follow?current_user_id=2')
        self.assertStatus(reply, 404)
        self.assertDescription(reply, 'The specified userid does not exist')

        # The follower does not exists
        reply = self.client.post('users/1/follow?current_user_id=8')
        self.assertStatus(reply, 404)
        self.assertDescription(reply, 'The specified current_user_id does not exist')

        # The user try to follow himself
        reply = self.client.post('users/1/follow?current_user_id=1')
        self.assertStatus(reply, 400)
        self.assertDescription(reply, "Can't follow yourself")

        # Get follower_counter of the user 1
        user = db.session.query(User).with_entities(User.follower_counter).filter(User.id == 1).first()
        follower_counter_old = user.follower_counter
        # Correct request
        reply = self.client.post('users/1/follow?current_user_id=2')
        self.assertStatus(reply, 200)
        # Check if follower_counter has been incremented
        user = db.session.query(User).with_entities(User.follower_counter).filter(User.id == 1).first()
        follower_counter_new = user.follower_counter
        self.assertEqual(follower_counter_new, (follower_counter_old + 1))

        # Try to follow again the same user
        reply = self.client.post('users/1/follow?current_user_id=2')
        self.assertStatus(reply, 400)
        self.assertDescription(reply, 'You already follow this storyteller')

    def test_unfollow(self):
        # Requests with bad parameters
        reply = self.client.post('users/1/unfollow?current_user_id=')
        self.assertStatus(reply, 400)
        self.assertDescription(reply, 'Error with current_user_id parameter')

        reply = self.client.post('users/1/unfollow?current_user_id=aa')
        self.assertStatus(reply, 400)
        self.assertDescription(reply, 'Error with current_user_id parameter')

        # The user to follow does not exist
        reply = self.client.post('users/6/unfollow?current_user_id=2')
        self.assertStatus(reply, 404)
        self.assertDescription(reply, 'The specified userid does not exist')

        # The follower does not exists
        reply = self.client.post('users/1/unfollow?current_user_id=8')
        self.assertStatus(reply, 404)
        self.assertDescription(reply, 'The specified current_user_id does not exist')

        # The user try to unfollow himself
        reply = self.client.post('users/1/unfollow?current_user_id=1')
        self.assertStatus(reply, 400)
        self.assertDescription(reply, "You can't follow yourself")

        # Let user 2 follows user 1
        reply = self.client.post('users/1/follow?current_user_id=2')
        self.assertStatus(reply, 200)

        # Get follower_counter of the user 1
        user = db.session.query(User).with_entities(User.follower_counter).filter(User.id == 1).first()
        follower_counter_old = user.follower_counter
        # Correct request
        reply = self.client.post('users/1/unfollow?current_user_id=2')
        self.assertStatus(reply, 200)
        # Check if follower_counter has been decremented
        user = db.session.query(User).with_entities(User.follower_counter).filter(User.id == 1).first()
        follower_counter_new = user.follower_counter
        self.assertEqual(follower_counter_new, (follower_counter_old - 1))

        # Try to unfollow again the same user
        reply = self.client.post('users/1/unfollow?current_user_id=2')
        self.assertStatus(reply, 400)
        self.assertDescription(reply, 'You should follow this storyteller before unfollowing')

    def test_followers(self):
        # Let user 2 follows user 1
        reply = self.client.post('users/1/follow?current_user_id=2')
        self.assertStatus(reply, 200)

        # Get user 1 followers
        reply = self.client.get('users/1/followers')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body, [
            {"email": "cantagallo@example.com", "firstname": "Cantagallo", "id": 2, "lastname": "Rooster"}
        ])

        # The user does not exist
        reply = self.client.get('users/8/followers')
        self.assertStatus(reply, 404)

    def test_search_exist_firstname(self):
        response = self.client.get('/search?query=Admin')
        body = json.loads(str(response.data, 'utf8'))
        self.assertEqual(body, [
            {"email": "example@example.com", "firstname": "Admin", "id": 1, "lastname": "Admin"}])

    def test_search_exist_lastname(self):
        response = self.client.get('/search?query=TheBest')
        body = json.loads(str(response.data, 'utf8'))
        self.assertEqual(body, [
            {"email": "thebest@example.com", "firstname": "Cantagallo", "id": 3, "lastname": "TheBest"}])

    def test_search_double_exist_firstname(self):
        response = self.client.get('/search?query=Cantagallo')
        body = json.loads(str(response.data, 'utf8'))
        self.assertEqual(body, [
            {"email": "cantagallo@example.com", "firstname": "Cantagallo", "id": 2, "lastname": "Rooster"},
            {"email": "thebest@example.com", "firstname": "Cantagallo", "id": 3, "lastname": "TheBest"}])

    def test_search_double_exist_lastname(self):
        response = self.client.get('/search?query=Rooster')
        body = json.loads(str(response.data, 'utf8'))
        self.assertEqual(body, [
            {"email": "cantagallo@example.com", "firstname": "Cantagallo", "id": 2, "lastname": "Rooster"},
            {"email": "theworst@example.com", "firstname": "TheWorst", "id": 4, "lastname": "Rooster"}])

    def test_search_not_exist(self):
        response = self.client.get('/search?query=notexist')
        self.assertStatus(response, 204)

    def test_search_bad_request(self):
        # NO parameter
        response = self.client.get('/search?=notexist')
        body = json.loads(str(response.data, 'utf8'))

        self.assertStatus(response, 400)
        self.assertEqual(body['description'],
                         'Error with query parameter')

        # Wrong parameter
        response = self.client.get('/search?notquery=notexist')
        body = json.loads(str(response.data, 'utf8'))

        self.assertStatus(response, 400)
        self.assertEqual(body['description'],
                         'Error with query parameter')

    def test_search_empty_request(self):
        response = self.client.get('/search?query=')
        self.assertStatus(response, 204)

    def test_user_stats(self):
        reply = self.client.get('users/1/stats')
        self.assertEqual(reply.status_code, 200)
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body, {"num_followers": 0, "followers_last_month": 0})

        # The user does not exist
        reply = self.client.get('users/180/stats')
        self.assertEqual(reply.status_code, 404)

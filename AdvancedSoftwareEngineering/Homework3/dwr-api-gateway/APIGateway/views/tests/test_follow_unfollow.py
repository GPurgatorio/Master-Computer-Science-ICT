import datetime

import flask_testing
from sqlalchemy.exc import IntegrityError

from monolith.app import create_app
from monolith.database import User, db, Follower
from monolith.forms import LoginForm
from monolith.urls import TEST_DB


class TestTemplateStories(flask_testing.TestCase):
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

            example2 = User()
            example2.firstname = 'Admin'
            example2.lastname = 'Admin'
            example2.email = 'example2@example2.com'
            example2.dateofbirth = datetime.datetime(2020, 10, 5)
            example2.is_admin = True
            example2.set_password('admin')
            db.session.add(example2)

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

    def test_login_required(self):
        response = self.client.post('/users/logout')
        # Log out success
        self.assert_redirects(response, '/')
        response = self.client.post('/users/{}/follow'.format(2), follow_redirects=True)
        self.assert401(response, 'You must login to follow')

        response = self.client.post('/users/{}/unfollow'.format(2), follow_redirects=True)
        self.assert401(response, 'You must login to unfollow')

    # FOLLOW

    def test_follow(self):
        self.client.post('/users/{}/follow'.format(2), follow_redirects=True)
        self.assert_template_used('wall.html')
        self.assert_message_flashed('Followed')

    def test_redirect_follow(self):
        response = self.client.post('/users/{}/follow'.format(2))
        self.assert_redirects(response, '/users/{}'.format(2))

    def test_already_follow(self):
        self.client.post('/users/{}/follow'.format(2), follow_redirects=True)
        self.client.post('/users/{}/follow'.format(2), follow_redirects=True)
        self.assert_template_used('wall.html')
        self.assert_message_flashed('You already follow this storyteller')

    def test_follow_yourself(self):
        self.client.post('/users/{}/follow'.format(1), follow_redirects=True)
        self.assert_template_used('wall.html')
        self.assert_message_flashed("You can't follow yourself")

    def test_follow_storyteller_no_exit(self):
        self.client.post('/users/{}/follow'.format(7), follow_redirects=True)
        self.assert_template_used('wall.html')
        self.assert_message_flashed("Storyteller doesn't exist")

    # UNFOLLOW

    def test_unfollow(self):
        self.client.post('/users/{}/follow'.format(2))
        self.client.post('/users/{}/unfollow'.format(2), follow_redirects=True)
        self.assert_template_used('wall.html')
        self.assert_message_flashed('Unfollowed')

    def test_redirect_unfollow(self):
        response = self.client.post('/users/{}/unfollow'.format(2))
        self.assert_redirects(response, '/users/{}'.format(2))

    def test_follow_first_to_unfollow(self):
        self.client.post('/users/{}/unfollow'.format(2), follow_redirects=True)
        self.assert_template_used('wall.html')
        self.assert_message_flashed('You should follow him first')

    def test_unfollow_yourself(self):
        self.client.post('/users/{}/unfollow'.format(1), follow_redirects=True)
        self.assert_template_used('wall.html')
        self.assert_message_flashed("You can't unfollow yourself")

    def test_unfollow_storyteller_no_exist(self):
        self.client.post('/users/{}/unfollow'.format(7), follow_redirects=True)
        self.assert_template_used('wall.html')
        self.assert_message_flashed("Storyteller doesn't exist")

    # DB CONSTRAINTS

    def test_only_positive_follower_counter(self):
        with self.assertRaises(IntegrityError):
            db.session.query(User).filter_by(id=1).update({'follower_counter': -1})

    def test_db_constraint_follow_yourself(self):
        with self.assertRaises(IntegrityError):
            follower = Follower()
            follower.followed_id = 1
            follower.follower_id = 1
            db.session.add(follower)
            db.session.commit()

    # TEST FOLLOWERS
    # Testing followers of non existing user
    def test_followers(self):
        self.client.get('/users/{}/followers'.format(7), follow_redirects=True)
        self.assert_template_used('wall.html')
        self.assert_message_flashed("Storyteller doesn't exist")

    # Testing followers of existing user
    def test_followers2(self):
        self.client.get('/users/{}/followers'.format(1), follow_redirects=True)
        self.assert_template_used('followers.html')

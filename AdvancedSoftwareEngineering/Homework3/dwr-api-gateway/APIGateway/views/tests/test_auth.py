import datetime

import flask_testing

from monolith.app import create_app
from monolith.database import Story, User, db
from monolith.forms import LoginForm
from monolith.urls import TEST_DB


class TestLoginLogout(flask_testing.TestCase):
    app = None

    def create_app(self):
        global app
        app = create_app(database=TEST_DB)
        return app

    # Set up database for testing here
    def setUp(self) -> None:
        with app.app_context():
            # create an user Admin
            example = User()
            example.firstname = 'Admin'
            example.lastname = 'Admin'
            example.email = 'example@example.com'
            example.dateofbirth = datetime.datetime(2010, 10, 5)
            example.is_admin = True
            example.set_password('admin')
            db.session.add(example)
            db.session.commit()

    # Executed at end of each test
    def tearDown(self) -> None:
        print("TEAR DOWN")
        db.session.remove()
        db.drop_all()

    def test_login_logout(self):
        # Test login with an unexisting email
        payload = {'email': 'unexisting@example.com',
                   'password': 'admin'}
        form = LoginForm(data=payload)
        self.client.post('/users/login', data=form.data, follow_redirects=True)
        self.assert_template_used('login.html')
        self.assert_message_flashed('This email does not exist.', 'error')

        # Test login with wrong password
        payload = {'email': 'example@example.com',
                   'password': 'wrong'}
        form = LoginForm(data=payload)
        self.client.post('/users/login', data=form.data, follow_redirects=True)
        self.assert_template_used('login.html')
        self.assert_message_flashed('Password is incorrect.', 'error')

        # Test successful login
        payload = {'email': 'example@example.com',
                   'password': 'admin'}
        form = LoginForm(data=payload)
        self.client.post('/users/login', data=form.data, follow_redirects=True)
        self.assert_template_used('index.html')
        all_stories = db.session.query(Story).all()
        self.assertEqual(self.get_context_variable('stories').all(), all_stories)

        # Test successful logout
        self.client.post('/users/logout', follow_redirects=True)
        self.assert_template_used('index.html')
        self.assertIsNone(self.get_context_variable('stories'))

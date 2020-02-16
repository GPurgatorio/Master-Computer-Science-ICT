import datetime

import flask_testing

from monolith.app import create_app
from monolith.database import db, User
from monolith.forms import UserForm
from monolith.urls import TEST_DB


class TestRegister(flask_testing.TestCase):
    app = None

    # First thing called
    def create_app(self):
        global app
        app = create_app(database=TEST_DB)
        return app

    # Set up database for testing here
    def setUp(self) -> None:
        with app.app_context():
            # create an user
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

    # Executed at end of each test
    def tearDown(self) -> None:
        print("TEAR DOWN")
        db.session.remove()
        db.drop_all()

    # Test /users/create
    def test_register(self):
        # Register an user with an already used email
        payload = {'email': 'example@example.com',
                   'firstname': 'Admin',
                   'lastname': 'Admin',
                   'password': 'admin',
                   'dateofbirth': datetime.datetime(2010, 10, 10).strftime('%d/%m/%Y')}
        form = UserForm(data=payload)
        self.client.post('/users/create', data=form.data, follow_redirects=True)
        self.assert_template_used('create_user.html')
        self.assert_message_flashed('The email address is already being used.', 'error')

        # Register an user with date of birth > today
        payload = {'email': 'example1@example.com',
                   'firstname': 'Admin',
                   'lastname': 'Admin',
                   'password': 'admin',
                   'dateofbirth': datetime.datetime(2020, 10, 10).strftime('%d/%m/%Y')}
        form = UserForm(data=payload)
        self.client.post('/users/create', data=form.data, follow_redirects=True)
        self.assert_template_used('create_user.html')
        self.assert_message_flashed('Wrong date of birth.', 'error')

        # Test successful registration
        payload = {'email': 'example1@example.com',
                   'firstname': 'Admin',
                   'lastname': 'Admin',
                   'password': 'admin',
                   'dateofbirth': datetime.datetime(2010, 10, 10).strftime('%d/%m/%Y')}
        form = UserForm(data=payload)
        self.client.post('/users/create', data=form.data, follow_redirects=True)
        self.assert_template_used('users.html')
        new_user = db.session.query(User).filter(User.email == 'example1@example.com').first()
        self.assertIsNotNone(new_user)

import datetime

import flask_testing

from monolith.app import create_app
from monolith.database import User, db
from monolith.forms import LoginForm
from monolith.urls import TEST_DB


class TestOtherWall(flask_testing.TestCase):
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

    def test_wall_login(self):
        # looking for non-existing user after login
        user_id = 100
        self.client.get('/users/{}'.format(user_id), follow_redirects=True)
        self.assert_template_used('wall.html')
        self.assertEqual(self.get_context_variable('not_found'), True)

        # looking for existing user after login
        user_id = 2
        self.client.get('/users/{}'.format(user_id), follow_redirects=True)
        self.assert_template_used('wall.html')
        self.assertEqual(self.get_context_variable('not_found'), False)
        self.assertEqual(self.get_context_variable('my_wall'), False)

        # looking for personal wall after login
        user_id = 1
        self.client.get('/users/{}'.format(user_id), follow_redirects=True)
        self.assert_template_used('wall.html')
        self.assertEqual(self.get_context_variable('not_found'), False)
        self.assertEqual(self.get_context_variable('my_wall'), True)

    def test_wall_nologin(self):
        response = self.client.post('/users/logout')
        # Log out success
        self.assert_redirects(response, '/')

        # looking for non-existing user without login
        user_id = 100
        self.client.get('/users/{}'.format(user_id), follow_redirects=True)
        self.assert_template_used('wall.html')
        self.assertEqual(self.get_context_variable('not_found'), True)

        # looking for existing user without login
        user_id = 1
        self.client.get('/users/{}'.format(user_id), follow_redirects=True)
        self.assert_template_used('wall.html')
        self.assertEqual(self.get_context_variable('not_found'), False)
        self.assertEqual(self.get_context_variable('my_wall'), False)

    # test method not allowed
    def test_methods_wall(self):
        self.assert405(self.client.post('/users/1'))
        self.assert405(self.client.put('/users/1'))
        self.assert405(self.client.delete('/users/1'))

import datetime

import flask_testing

from monolith.app import create_app
from monolith.database import Story, User, db, Counter
from monolith.forms import LoginForm
from monolith.urls import TEST_DB


class TestUsers(flask_testing.TestCase):
    app = None

    def create_app(self):
        global app
        app = create_app(database=TEST_DB)
        return app

    # Set up database for testing here
    def setUp(self) -> None:
        print("SET UP")
        with app.app_context():
            # Add Admin user
            example = User()
            example.firstname = 'Admin'
            example.lastname = 'Admin'
            example.email = 'example@example.com'
            example.dateofbirth = datetime.datetime(2020, 10, 5)
            example.is_admin = True
            example.set_password('admin')
            db.session.add(example)

            # Add another user for testing
            example = User()
            example.firstname = 'Test'
            example.lastname = 'Man'
            example.email = 'test@test.com'
            example.dateofbirth = datetime.datetime(2020, 10, 6)
            example.is_admin = False
            example.set_password('test')
            db.session.add(example)

            # Add some stories for user 1
            example = Story()
            example.text = 'Trial story of example admin user :)'
            example.author_id = 1
            example.figures = '#example#admin#'
            example.is_draft = False
            db.session.add(example)
            db.session.commit()

            example = Story()
            example.text = 'Another story!'
            example.author_id = 1
            example.is_draft = True
            example.figures = '#another#story#'
            db.session.add(example)
            db.session.commit()

            # Add reactions for user 1
            like = Counter()
            like.reaction_type_id = 1
            like.story_id = 1
            like.counter = 23
            dislike = Counter()
            dislike.reaction_type_id = 2
            dislike.story_id = 1
            dislike.counter = 5
            db.session.add(like)
            db.session.add(dislike)
            db.session.commit()

            # login
            payload = {'email': 'example@example.com',
                       'password': 'admin'}

            form = LoginForm(data=payload)

            self.client.post('/users/login', data=form.data, follow_redirects=True)

    # Executed at end of each test
    def tearDown(self) -> None:
        print("TEAR DOWN")
        db.session.remove()
        db.drop_all()

    def test_user_stories(self):
        # Testing stories of not existing user
        response = self.client.get('/users/100/stories')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://127.0.0.1:5000/')

        # Testing stories of existing user
        response = self.client.get('/users/1/stories')
        self.assert200(response)
        self.assert_template_used('user_stories.html')

    def test_user_drafts(self):
        # Testing stories of not existing user
        response = self.client.get('/users/100/drafts')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://127.0.0.1:5000/')

        # Testing stories of other user
        response = self.client.get('/users/2/drafts')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://127.0.0.1:5000/')

        # Testing stories of existing user
        response = self.client.get('/users/1/drafts')
        self.assert200(response)
        self.assert_template_used('drafts.html')

    def test_user_statistics(self):
        self.client.get('/users/1')
        self.assert_template_used('wall.html')
        # I should be logged as admin so i'm looking for my wall
        self.assertEqual(self.get_context_variable('my_wall'), True)
        num_stories = Story.query.filter_by(author_id=1).count()
        self.assertEqual(self.get_context_variable('stats')[2][1], num_stories)
        reactions = 28  # 23 Likes + 5 Dislikes
        self.assertEqual(self.get_context_variable('stats')[1][1], reactions)
        avg_dice = 2.0  # every story has 2 figures
        self.assertEqual(self.get_context_variable('stats')[3][1], avg_dice)
        avg_reactions = 14
        self.assertEqual(self.get_context_variable('stats')[0][1], avg_reactions)

    def test_someone_statistics(self):
        self.client.get('/users/2')
        self.assert_template_used('wall.html')
        # I should be logged as admin and looking for someone's wall
        self.assertEqual(self.get_context_variable('my_wall'), False)
        num_stories = Story.query.filter_by(author_id=2).count()
        self.assertEqual(self.get_context_variable('stats')[1][1], num_stories)
        # There aren't statistics for this user (num_reactions) 
        self.assertEqual(self.get_context_variable('stats')[0][1], 0)

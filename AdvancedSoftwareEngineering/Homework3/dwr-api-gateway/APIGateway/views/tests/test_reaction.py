import datetime

import flask_testing

from monolith.app import create_app
from monolith.database import db, Reaction, User, Story
from monolith.forms import LoginForm
from monolith.urls import TEST_DB


class TestReaction(flask_testing.TestCase):
    app = None

    def create_app(self):
        global app
        app = create_app(database=TEST_DB)
        return app

    def setUp(self) -> None:
        with app.app_context():
            # user for login
            example = User()
            example.firstname = 'Admin'
            example.lastname = 'Admin'
            example.email = 'example@example.com'
            example.dateofbirth = datetime.datetime(2020, 10, 5)
            example.is_admin = True
            example.set_password('admin')
            db.session.add(example)
            db.session.commit()

            # reacted story
            test_story = Story()
            test_story.text = "Test story from admin user"
            test_story.author_id = 1
            test_story.is_draft = 0
            test_story.figures = "#Test#admin#"
            db.session.add(test_story)
            db.session.commit()

            # login
            payload = {'email': 'example@example.com',
                       'password': 'admin'}

            form = LoginForm(data=payload)

            self.client.post('/users/login', data=form.data, follow_redirects=True)

    def test_reaction(self):
        len_to_be_deleted_reactions = len(Reaction.query.filter(Reaction.story_id == '1',
                                                                Reaction.reactor_id == 1,
                                                                Reaction.marked == 2).all())

        self.client.post('http://127.0.0.1:5000/stories/1/react/like', follow_redirects=True)

        self.assert_template_used('story.html')
        unmarked_reactions = Reaction.query.filter(Reaction.story_id == '1',
                                                   Reaction.reactor_id == 1,
                                                   Reaction.marked == 0).all()

        self.assertEqual(len(unmarked_reactions), 1)
        self.assertEqual(unmarked_reactions[0].reaction_type_id, 1)

        self.client.post('http://127.0.0.1:5000/stories/1/react/like')
        self.assert_template_used('story.html')
        self.assert_message_flashed('Reaction successfully deleted! (Updating ... )')

        self.client.post('http://127.0.0.1:5000/stories/1/react/dislike')
        self.assert_template_used('story.html')
        unmarked_reactions = Reaction.query.filter(Reaction.story_id == '1', Reaction.marked == 0).all()
        self.assertEqual(unmarked_reactions[0].reaction_type_id, 2)
        self.assertEqual(len(unmarked_reactions), 1)

        Reaction.query.filter(Reaction.story_id == '1', Reaction.marked == 0).first().marked = 1
        db.session.commit()

        self.client.post('http://127.0.0.1:5000/stories/1/react/like')
        unmarked_reactions = Reaction.query.filter(Reaction.story_id == '1',
                                                   Reaction.reactor_id == 1,
                                                   Reaction.marked == 0).all()

        marked_reactions = Reaction.query.filter(Reaction.story_id == '1',
                                                 Reaction.reactor_id == 1,
                                                 Reaction.marked == 1).all()

        to_be_deleted_reactions = Reaction.query.filter(Reaction.story_id == '1',
                                                        Reaction.reactor_id == 1,
                                                        Reaction.marked == 2).all()

        self.assertEqual(len(unmarked_reactions), 1)
        self.assertEqual(len(marked_reactions), 0)
        self.assertEqual(len(to_be_deleted_reactions), len_to_be_deleted_reactions + 1)

    def test_reaction_1(self):
        self.client.post('http://127.0.0.1:5000/stories/1/react/like')
        self.client.post('http://127.0.0.1:5000/stories/1/react/dislike')

        unmarked_reactions = Reaction.query.filter(Reaction.story_id == '1',
                                                   Reaction.reactor_id == 1,
                                                   Reaction.marked == 0).all()

        self.assertEqual(len(unmarked_reactions), 1)
        self.assertEqual(unmarked_reactions[0].reaction_type_id, 2)

        Reaction.query.filter(Reaction.story_id == '1', Reaction.reactor_id == 1,
                              Reaction.marked == 0).first().marked = 1
        db.session.commit()

        self.client.post('http://127.0.0.1:5000/stories/1/react/dislike')
        self.assertEqual(Reaction.query.filter(Reaction.story_id == '1', Reaction.reactor_id == 1).first().marked, 2)

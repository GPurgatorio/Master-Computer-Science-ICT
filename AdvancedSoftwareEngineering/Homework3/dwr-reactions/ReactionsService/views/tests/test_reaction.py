import json

import flask_testing

from unittest.mock import Mock, patch
from ReactionsService.app import create_app
from ReactionsService.database import db, Reaction, Counter, ReactionCatalogue
from ReactionsService.urls import TEST_DB
from ReactionsService.views.tests.mock import start_mock_server, get_free_port


class TestReaction(flask_testing.TestCase):
    app = None

    def create_app(self):
        global app
        app = create_app(database=TEST_DB)
        return app

    # def setUp(self) -> None:
    #     with app.app_context():

    def test_reaction(self):
        len_to_be_deleted_reactions = len(Reaction.query.filter(Reaction.story_id == '1',
                                                                Reaction.reactor_id == 1,
                                                                Reaction.marked == 2).all())

        data = {
            'story_id': 1,
            'current_user': 1,
            'reaction_caption': 'like',
        }
        self.client.post('/react', json=data)

        unmarked_reactions = Reaction.query.filter(Reaction.story_id == '1',
                                                   Reaction.reactor_id == 1,
                                                   Reaction.marked == 0).all()

        self.assertEqual(len(unmarked_reactions), 1)
        self.assertEqual(unmarked_reactions[0].reaction_type_id, 1)

        data = {
            'story_id': 1,
            'current_user': 1,
            'reaction_caption': 'like',
        }

        self.client.post('/react', json=data)
        # self.assert_message_flashed('Reaction successfully deleted! (Updating ... )')

        data = {
            'story_id': 1,
            'current_user': 1,
            'reaction_caption': 'dislike',
        }

        self.client.post('/react', json=data)
        unmarked_reactions = Reaction.query.filter(Reaction.story_id == '1', Reaction.marked == 0).all()
        self.assertEqual(unmarked_reactions[0].reaction_type_id, 2)
        self.assertEqual(len(unmarked_reactions), 1)

        Reaction.query.filter(Reaction.story_id == '1', Reaction.marked == 0).first().marked = 1
        db.session.commit()

        data = {
            'story_id': 1,
            'current_user': 1,
            'reaction_caption': 'like',
        }

        self.client.post('/react', json=data)
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
        data = {
            'story_id': 1,
            'current_user': 1,
            'reaction_caption': 'like',
        }

        self.client.post('/react', json=data)

        data = {
            'story_id': 1,
            'current_user': 1,
            'reaction_caption': 'dislike',
        }

        self.client.post('/react', json=data)

        unmarked_reactions = Reaction.query.filter(Reaction.story_id == '1',
                                                   Reaction.reactor_id == 1,
                                                   Reaction.marked == 0).all()

        self.assertEqual(len(unmarked_reactions), 1)
        self.assertEqual(unmarked_reactions[0].reaction_type_id, 2)

        Reaction.query.filter(Reaction.story_id == '1', Reaction.reactor_id == 1,
                              Reaction.marked == 0).first().marked = 1
        db.session.commit()

        data = {
            'story_id': 1,
            'current_user': 1,
            'reaction_caption': 'dislike',
        }

        self.client.post('/react', json=data)
        self.assertEqual(Reaction.query.filter(Reaction.story_id == '1', Reaction.reactor_id == 1).first().marked, 2)

    def test_get_reactions(self):
        data = {
            'story_id': 1,
            'current_user': 1,
            'reaction_caption': 'like',
        }

        self.client.post('/react', json=data)
        reply = self.client.get('/reactions/1')

        body = json.loads(reply.get_data(as_text=True))
        expected_body = [{"id": 1, "reactor_id": 1, "story_id": 1, "reaction_type_id": 1, "marked": 0}]
        self.assertEqual(expected_body, body)

    def test_get_counters(self):
        data = {
            'story_id': 1,
        }
        self.client.post('/new', json=data)

        reply = self.client.get('/counters/1')

        body = json.loads(reply.get_data(as_text=True))
        expected_body = [{"reaction_type_id": 1, "story_id": 1, "counter": 0},
                         {"reaction_type_id": 2, "story_id": 1, "counter": 0}]
        self.assertEqual(expected_body, body)

    def test_initialize_new_story(self):
        data = {
            'story_id': 1,
        }
        self.client.post('/new', json=data)

        types = ReactionCatalogue.query.all()
        counters = Counter.query.filter(Counter.story_id == 1).all()

        self.assertEqual(len(counters), len(types))

    def test_delete_cascade(self):
        data = {
            'story_id': 1,
        }
        self.client.post('/new', json=data)
        data = {
            'story_id': 1,
            'current_user': 1,
            'reaction_caption': 'like',
        }

        self.client.post('/react', json=data)

        data = {
            'story_id': 1,
        }

        self.client.delete("/delete", json=data)

        reactions = Reaction.query.filter(Reaction.story_id == 1).all()
        counters = Counter.query.filter(Counter.story_id == 1).all()

        self.assertEqual(len(counters), 0)
        self.assertEqual(len(reactions), 0)
    
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = 5003
        start_mock_server(cls.mock_server_port)
        
    def test_reactions_stats(self):
        # Check stats of story #1
        response = self.client.get('/reactions/stats/1')
        body = json.loads(str(response.data, 'utf8'))
        self.assertEqual(body, {"dislike": 0, "like": 0})

        # Add some reactions to a story
        example = Counter()
        example.story_id = 1
        example.reaction_type_id = 1
        example.counter = 3
        db.session.add(example)
        db.session.commit()

        # Check stats of story #2
        response = self.client.get('/reactions/stats/1')
        body = json.loads(str(response.data, 'utf8'))
        self.assertEqual(body, {"dislike": 0, "like": 3})


        # Check story's reactions statistics
        mock_reactions_stats_url = 'http://127.0.0.1:{port}/stories/users/'.format(port=self.mock_server_port)
        with patch.dict('ReactionsService.views.reactions.__dict__', {'USER_STORIES_URL': mock_reactions_stats_url}):
            response = self.client.get('/reactions/stats/users/1', content_type='application/json')
        body = json.loads(str(response.data, 'utf8'))
        print(body)
        self.assertStatus(response, 200)
        self.assertEqual(body['tot_num_reactions'], 3)
        self.assertEqual(body['avg_reactions'], 1.5)

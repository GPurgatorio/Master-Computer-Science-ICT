import datetime
import json

import flask_testing
from flask import jsonify
from unittest.mock import Mock, patch

from StoriesService.app import create_app
from StoriesService.database import db, Story
from StoriesService.urls import *

from StoriesService.views.test.mock import start_mock_server, get_free_port


class TestStories(flask_testing.TestCase):
    app = None

    # First thing called
    def create_app(self):
        global app
        app = create_app(database=TEST_DB)
        return app

    # Set up database for testing here
    def setUp(self) -> None:
        with app.app_context():
            # Create the first story, default from teacher's code
            example = Story()
            example.text = 'Trial story of example admin user :)'
            example.author_id = 1
            example.figures = '#example#admin#'
            example.is_draft = False
            example.date = datetime.datetime.strptime('2019-10-20', '%Y-%m-%d')
            db.session.add(example)
            db.session.commit()

            # Create a story that shouldn't be seen in /latest
            example = Story()
            example.text = 'Old story (dont see this in /latest)'
            example.date = datetime.datetime.strptime('2019-10-10', '%Y-%m-%d')
            example.author_id = 2
            example.is_draft = False
            example.figures = '#example#abc#'
            db.session.add(example)
            db.session.commit()

            # Create a story that should be seen in /latest
            example = Story()
            example.text = 'You should see this one in /latest'
            example.date = datetime.datetime.strptime('2019-10-13', '%Y-%m-%d')
            example.author_id = 2
            example.is_draft = False
            example.figures = '#example#abc#'
            db.session.add(example)
            db.session.commit()

            # Random draft from a non-admin user
            example = Story()
            example.text = 'DRAFT from not admin'
            example.date = datetime.datetime.strptime('2018-12-30', '%Y-%m-%d')
            example.author_id = 3
            example.is_draft = True
            example.figures = '#example#nini#'
            db.session.add(example)
            db.session.commit()

            # Create a very old story for range searches purpose
            example = Story()
            example.text = 'very old story (11 11 2011)'
            example.date = datetime.datetime.strptime('2011-11-11', '%Y-%m-%d')
            example.author_id = 3
            example.is_draft = False
            example.figures = '#example#nini#'
            example.date = datetime.datetime(2011, 11, 11)
            db.session.add(example)
            db.session.commit()

    # Executed at end of each test
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_all_stories(self):
        response = self.client.get('/stories')
        body = json.loads(str(response.data, 'utf8'))
        self.assertEqual(body, [
            {'author_id': 1, 'date': 'Sun, 20 Oct 2019 00:00:00 GMT', 'figures': '#example#admin#', 'id': 1,
             'is_draft': False, 'text': 'Trial story of example admin user :)'},
            {'author_id': 2, 'date': 'Sun, 13 Oct 2019 00:00:00 GMT', 'figures': '#example#abc#', 'id': 3,
             'is_draft': False, 'text': 'You should see this one in /latest'},
            {'author_id': 2, 'date': 'Thu, 10 Oct 2019 00:00:00 GMT', 'figures': '#example#abc#', 'id': 2,
             'is_draft': False, 'text': 'Old story (dont see this in /latest)'},
            {'author_id': 3, 'date': 'Fri, 11 Nov 2011 00:00:00 GMT', 'figures': '#example#nini#', 'id': 5,
             'is_draft': False, 'text': 'very old story (11 11 2011)'}])

    def test_existing_story(self):
        response = self.client.get('/stories/1')
        body = json.loads(str(response.data, 'utf8'))
        test_story = Story.query.filter_by(id=1).first()
        self.assertEqual(body['text'], test_story.to_json()['text'])
        self.assertEqual(body['author_id'], test_story.to_json()['author_id'])

    def test_non_existing_story(self):
        response = self.client.get('/stories/50')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 404)
        self.assertEqual(body['description'], 'Specified story not found')

    def test_stories_user(self):
        response = self.client.get('/stories/users/1')
        body = json.loads(str(response.data, 'utf8'))
        self.assertEqual(body, [{'author_id': 1, 'date': 'Sun, 20 Oct 2019 00:00:00 GMT', 'figures': '#example#admin#',
                                'id': 1, 'is_draft': False, 'text': 'Trial story of example admin user :)'}])

    def test_non_existing_user(self):
        response = self.client.get('/stories/users/50')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 404)
        self.assertEqual(body['description'], 'Stories of specified user not found')

    # Testing that the oldest story per user is contained in the resulting stories
    def test_latest_story(self):
        response = self.client.get('/stories/latest')
        body = json.loads(str(response.data, 'utf8'))
        self.assertEqual(body,
                         [
                             {'author_id': 1, 'date': 'Sun, 20 Oct 2019 00:00:00 GMT', 'figures': '#example#admin#',
                              'id': 1,
                              'is_draft': False, 'text': 'Trial story of example admin user :)'},
                             {'author_id': 2, 'date': 'Sun, 13 Oct 2019 00:00:00 GMT', 'figures': '#example#abc#',
                              'id': 3,
                              'is_draft': False, 'text': 'You should see this one in /latest'},
                             {'author_id': 3, 'date': 'Fri, 11 Nov 2011 00:00:00 GMT', 'figures': '#example#nini#',
                              'id': 5,
                              'is_draft': False, 'text': 'very old story (11 11 2011)'}
                         ]
                         )

    # Testing range story with possible inputs
    def test_range_story(self):
        # Testing range without parameters
        # Expected behaviour: it should return ALL the stories
        response = self.client.get('/stories/range')
        all_stories = db.session.query(Story).filter_by(is_draft=False).all()
        all_storiesJ = jsonify([story.to_json() for story in all_stories])
        self.assertStatus(response, 200)
        self.assertEqual(response.data, all_storiesJ.data)

        # Testing range with only one parameter (begin)
        # Expected behaviour: it should return the stories starting from specified date to TODAY
        response = self.client.get('/stories/range?begin=2013-10-10')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 200)
        self.assertEqual(body, [
            {'author_id': 1, 'date': 'Sun, 20 Oct 2019 00:00:00 GMT', 'figures': '#example#admin#', 'id': 1,
             'is_draft': False, 'text': 'Trial story of example admin user :)'},
            {'author_id': 2, 'date': 'Thu, 10 Oct 2019 00:00:00 GMT', 'figures': '#example#abc#', 'id': 2,
             'is_draft': False, 'text': 'Old story (dont see this in /latest)'},
            {'author_id': 2, 'date': 'Sun, 13 Oct 2019 00:00:00 GMT', 'figures': '#example#abc#', 'id': 3,
             'is_draft': False, 'text': 'You should see this one in /latest'}])

        # Testing range with only one parameter (end)
        # Expected behaviour: it should return all the stories BEFORE the specified date
        response = self.client.get('/stories/range?end=2013-10-10')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 200)
        self.assertEqual(body, [
            {'author_id': 3, 'date': 'Fri, 11 Nov 2011 00:00:00 GMT', 'figures': '#example#nini#', 'id': 5,
             'is_draft': False, 'text': 'very old story (11 11 2011)'}])

        # Testing range with begin date > end date
        response = self.client.get('/stories/range?begin=2012-12-12&end=2011-10-10')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 400)
        self.assertEqual(body['description'], 'Begin date cannot be higher than End date')

        # Testing range with wrong url parameters
        response = self.client.get('/stories/range?begin=abc&end=abc')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 400)
        self.assertEqual(body['description'], 'Wrong URL parameters')

        # Testing range with a valid request
        # Expected behaviour: return all the stories between the specified dates
        response = self.client.get('/stories/range?begin=2012-10-15&end=2020-10-10')
        body = json.loads(str(response.data, 'utf8'))
        self.assertEqual(body, [
            {'author_id': 1, 'date': 'Sun, 20 Oct 2019 00:00:00 GMT', 'figures': '#example#admin#', 'id': 1,
             'is_draft': False, 'text': 'Trial story of example admin user :)'},
            {'author_id': 2, 'date': 'Thu, 10 Oct 2019 00:00:00 GMT', 'figures': '#example#abc#', 'id': 2,
             'is_draft': False, 'text': 'Old story (dont see this in /latest)'},
            {'author_id': 2, 'date': 'Sun, 13 Oct 2019 00:00:00 GMT', 'figures': '#example#abc#', 'id': 3,
             'is_draft': False, 'text': 'You should see this one in /latest'}]
                         )

    def test_drafts(self):
        response = self.client.get('/stories/range?begin=2013-10-10')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 200)
        self.assertEqual(body, [
            {'author_id': 1, 'date': 'Sun, 20 Oct 2019 00:00:00 GMT', 'figures': '#example#admin#', 'id': 1,
             'is_draft': False, 'text': 'Trial story of example admin user :)'},
            {'author_id': 2, 'date': 'Thu, 10 Oct 2019 00:00:00 GMT', 'figures': '#example#abc#', 'id': 2,
             'is_draft': False, 'text': 'Old story (dont see this in /latest)'},
            {'author_id': 2, 'date': 'Sun, 13 Oct 2019 00:00:00 GMT', 'figures': '#example#abc#', 'id': 3,
             'is_draft': False, 'text': 'You should see this one in /latest'}])

        # Testing range with only one parameter (end)
        # Expected behaviour: it should return all the stories BEFORE the specified date
        response = self.client.get('/stories/range?end=2013-10-10')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 200)
        self.assertEqual(body, [
            {'author_id': 3, 'date': 'Fri, 11 Nov 2011 00:00:00 GMT', 'figures': '#example#nini#', 'id': 5,
             'is_draft': False, 'text': 'very old story (11 11 2011)'}])

    def test_statistics(self):
        # Test stories statistics
        # Expected behaviour: return 2 stories, 4 total dice and 2.0 avg dice
        response = self.client.get('/stories/stats/2')
        body = json.loads(str(response.data, 'utf8'))
        all_stories = db.session.query(Story).filter_by(is_draft=False).all()
        self.assertStatus(response, 200)
        self.assertEqual(body, {'num_stories': 2, 'tot_num_dice': 4, 'avg_dice': 2.0})

    def test_draft(self):
        response = self.client.get('/stories/drafts?user_id=2')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 404)
        self.assertEqual(body['description'], 'There are no recent drafts by this user')

        response = self.client.get('/stories/drafts?user_id=3')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 200)
        self.assertEqual(body, [
            {"author_id": 3, "date": "Sun, 30 Dec 2018 00:00:00 GMT", "figures": "#example#nini#", "id": 4,
             "is_draft": True, "text": "DRAFT from not admin"}]
                         )
        response = self.client.get('/stories/drafts?use_id=3')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 400)
        self.assertEqual(body['description'], 'Invalid parameters')

    @classmethod
    def setup_class(cls):
        cls.mock_server_port = 5004
        cls.mock_server = start_mock_server(cls.mock_server_port)

    def test_write_story(self):
        mock_users_url = 'http://localhost:{port}/new'.format(port=self.mock_server_port)
        # Testing publishing valid story
        with patch.dict('StoriesService.views.stories.__dict__', {'NEW_REACTIONS_URL': mock_users_url}):
            payload = {'text': 'my cat is drinking a beer with my neighbour\'s dog', 'figures': '#beer#cat#dog#',
                       'as_draft': False, 'user_id': '1'}
            response = self.client.post('/stories', data=json.dumps(payload), content_type='application/json')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 201)
        self.assertEqual(body['description'], 'New story has been published')

        # Testing invalid request
        payload = {'text': 'my cat is drinking a gin tonic with my neighbour\'s dog', 'figures': '',
                   'as_draft': 'a',
                   'user': 'b'}
        response = self.client.post('/stories', data=json.dumps(payload), content_type='application/json')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 400)
        self.assertEqual(body['description'], 'Wrong parameters')

        # Testing publishing invalid story
        payload = {'text': 'my cat is drinking a gin tonic with my neighbour\'s dog', 'figures': '#beer#cat#dog#',
                   'as_draft': False, 'user_id': '1'}
        response = self.client.post('/stories', data=json.dumps(payload), content_type='application/json')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 422)
        self.assertEqual(body['description'], 'Your story doesn\'t contain all the words. Missing: beer ')

        payload = {'text': 'a' * 1001, 'figures': '#beer#cat#dog#',
                   'as_draft': False, 'user_id': '1'}
        response = self.client.post('/stories', data=json.dumps(payload), content_type='application/json')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 422)
        self.assertEqual(body['description'], 'Story is too long')

        # Testing writing of other user's draft
        payload = {'text': 'my cat is drinking a gin tonic with my neighbour\'s dog', 'as_draft': True,
                   'user_id': '2'}
        response = self.client.put('/stories/4', data=json.dumps(payload), content_type='application/json')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 403)
        self.assertEqual(body['description'],
                         'Request is invalid, check if you are the author of the story and it is still a draft')

        # Testing writing of an already published story
        response = self.client.put('/stories/4', data=json.dumps(payload), content_type='application/json')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 403)
        self.assertEqual(body['description'],
                         'Request is invalid, check if you are the author of the story and it is still a draft')

        # Testing saving a new story as draft
        payload2 = {'text': 'my cat is drinking', 'figures': '#beer#cat#dog#', 'as_draft': True, 'user_id': 1}
        response = self.client.post('/stories', data=json.dumps(payload2), content_type='application/json')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 201)
        self.assertEqual(body['description'], 'Draft created')

        # Testing saving a draft again
        count = db.session.query(Story).count()
        response = self.client.put('/stories/7', data=json.dumps(payload2), content_type='application/json')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 200)
        self.assertEqual(body['description'], 'Draft updated')
        # No items added
        q = db.session.query(Story).filter(Story.id == count + 1).first()
        self.assertEqual(q, None)

        # Testing publishing an invalid draft story
        payload3 = {'text': 'my cat is drinking and beer', 'as_draft': False, 'user_id': '1'}
        response = self.client.put('/stories/7', data=json.dumps(payload3), content_type='application/json')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 422)
        self.assertEqual(body['description'], 'Your story doesn\'t contain all the words. Missing: dog ')

        # Testing publishing a draft story
        count = db.session.query(Story).count()
        payload3 = {'text': 'my cat is drinking dog and beer', 'as_draft': False, 'user_id': '1'}
        response = self.client.put('/stories/7', data=json.dumps(payload3), content_type='application/json')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 200)
        self.assertEqual(body['description'], 'Story published')
        q = db.session.query(Story).filter(Story.id == count + 1).first()
        self.assertEqual(q, None)
        q = db.session.query(Story).filter(Story.id == 6).first()
        self.assertEqual(q.is_draft, False)

        # Errors in request body
        payload3 = {'tet': 'my cat is drinking dog and beer', 'as_draft': False, 'user_id': '1'}
        response = self.client.put('/stories/7', data=json.dumps(payload3), content_type='application/json')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 400)
        self.assertEqual(body['description'], 'Errors in request body')

    def test_delete_story(self):
        # Deleting the story of another user
        payload4 = {'user_id': 2}
        response = self.client.delete('/stories/1', data=json.dumps(payload4), content_type='application/json')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 400)
        self.assertEqual(body['description'],
                         'Request is invalid, check if you are the author of the story and the id is a valid one')

        # Deleting your story
        mock_users_url = 'http://localhost:{port}/delete'.format(port=self.mock_server_port)
        #Testing deleting valid story
        with patch.dict('StoriesService.views.stories.__dict__', {'DELETE_REACTIONS_URL': mock_users_url}):
            payload4 = {'user_id': 1}
            response = self.client.delete('/stories/1', data=json.dumps(payload4), content_type='application/json')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 200)
        self.assertEqual(body['description'],
                         'Story has been deleted')

    def test_search_exist(self):
        response = self.client.get('/search?query=nini')
        body = json.loads(str(response.data, 'utf8'))
        self.assertEqual(body, [
            {'author_id': 3, 'date': 'Fri, 11 Nov 2011 00:00:00 GMT', 'figures': '#example#nini#', 'id': 5,
             'is_draft': False, 'text': 'very old story (11 11 2011)'}])
    
    def test_search_double_exist(self):
        response = self.client.get('/search?query=abc')
        body = json.loads(str(response.data, 'utf8'))
        self.assertEqual(body, [
            {'author_id': 2, 'date': 'Thu, 10 Oct 2019 00:00:00 GMT', 'figures': '#example#abc#', 'id': 2,
             'is_draft': False, 'text': 'Old story (dont see this in /latest)'},
            {'author_id': 2, 'date': 'Sun, 13 Oct 2019 00:00:00 GMT', 'figures': '#example#abc#', 'id': 3,
             'is_draft': False, 'text': 'You should see this one in /latest'}])

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

class TestRandomRecentStory(flask_testing.TestCase):
    app = None

    # First thing called
    def create_app(self):
        global app
        app = create_app(database=TEST_DB)
        return app

    # Set up database for testing here
    def setUp(self) -> None:
        with app.app_context():
            # Create a not recent story by Admin2
            example = Story()
            example.text = 'This is a story about the end of the world'
            example.date = datetime.datetime.strptime('2012-12-12', '%Y-%m-%d')
            example.author_id = 2
            example.figures = '#story#world#'
            example.is_draft = False
            db.session.add(example)
            db.session.commit()

            # Create a recent story saved as draft by Admin2
            example = Story()
            example.text = 'This story is just a draft'
            example.date = datetime.datetime.now()
            example.author_id = 2
            example.figures = '#story#draft#'
            example.is_draft = True
            db.session.add(example)
            db.session.commit()

            # Create a recent story by Admin
            example = Story()
            example.text = 'Just another story'
            example.date = datetime.datetime.now()
            example.author_id = 1
            example.figures = '#dice#example#'
            example.is_draft = False
            db.session.add(example)
            db.session.commit()

    def test_random_recent_story(self):
        # Random recent story as anonymous user
        response = self.client.get('/stories/random')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 200)
        self.assertEqual(body['text'], 'Just another story')

        # No recent stories
        response = self.client.get('/stories/random?user_id=1')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 404)
        self.assertEqual(body['description'], 'There are no recent stories by other users')

        # Create a new recent story by Admin2
        example = Story()
        example.text = 'This is a valid recent story'
        example.date = datetime.datetime.now()
        example.author_id = 2
        example.figures = 'story#recent'
        example.is_draft = False
        db.session.add(example)
        db.session.commit()

        # Get the only recent story not written by Admin
        response = self.client.get('/stories/random?user_id=1')
        body = json.loads(str(response.data, 'utf8'))
        self.assertStatus(response, 200)
        self.assertEqual(body['text'], 'This is a valid recent story')

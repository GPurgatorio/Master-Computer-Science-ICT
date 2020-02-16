import json

import flask_testing

from .app import create_app
from .database import db, DiceSet, Die
from .urls import TEST_DB


class TestDice(flask_testing.TestCase):
    app = None

    # First thing called
    def create_app(self):
        global app
        app = create_app(database=TEST_DB)
        return app

    def tearDown(self) -> None:
        print("TEAR DOWN")
        db.session.remove()
        db.drop_all()

    def assertDescription(self, response, expected_description):
        body = json.loads(str(response.data, 'utf8'))
        self.assertEqual(body['description'], expected_description)

    def test_add_set(self):
        # create without body
        result = self.client.post('/sets', data=None)
        self.assert400(result)
        self.assertDescription(result, "Not valid request body")

        # create without specifing name / dice array
        data = {"name": "TestSet"}
        result = self.client.post('/sets', data=json.dumps(data), content_type='application/json')
        self.assert400(result)
        self.assertDescription(result, "Name or dice are missing")

        data = {"dice": []}
        result = self.client.post('/sets', data=json.dumps(data), content_type='application/json')
        self.assert400(result)
        self.assertDescription(result, "Name or dice are missing")

        # create with less than 6 dice
        data = {"name": "TestSet",
                "dice": [
                    ["bike", "moonandstars", "bag", "bird", "crying", "angry"],
                    ["tulip", "mouth", "caravan", "clock", "whale", "drink"],
                ]}
        result = self.client.post('/sets', data=json.dumps(data), content_type='application/json')
        self.assert400(result)
        self.assertDescription(result, "DiceSet must be formed by 6 dice of 6 figures each one")

        # create with 6 dice (some incomplete)
        data = {"name": "TestSet",
                "dice": [
                    ["bike", "moonandstars", "bag", "bird", "crying", "angry"],
                    ["tulip", "mouth", "caravan", "whale", "drink"],
                    ["happy", "coffee", "plate", "bus", "paws"],
                    ["cat", "pencil", "baloon", "bananas", "phone", "icecream"],
                    ["ladder", "car", "fir", "bang", "hat"],
                    ["rain", "heart", "glasses", "poo", "ball", "sun"]
                ]}
        result = self.client.post('/sets', data=json.dumps(data), content_type='application/json')
        self.assert400(result)
        self.assertDescription(result, "DiceSet must be formed by 6 dice of 6 figures each one")

        # create a DiceSet successfully
        data = {"name": "animal",
                "dice": [
                    ["bear", "cow", "elephant", "panda", "bull", "rhino"],
                    ["monkey", "bat", "lion", "tiger", "koala", "crocodile"],
                    ["whale", "penguin", "dolphin", "orca", "seahorses", "turtle"],
                    ["rabbit", "mouse", "cat", "chicken", "dog", "horse"],
                    ["fox", "squirrel", "frog", "butterfly", "donkey", "pork"],
                    ["eagle", "parrot", "rooster", "dragon", "sheep", "snake"]
                ]}

        result = self.client.post('/sets', data=json.dumps(data), content_type='application/json')
        self.assertStatus(result, 201)
        self.assertDescription(result, "DiceSet successfully added")

        # check that in the db there's 1 set and 6 dice
        set_counter = DiceSet.query.count()
        dice_counter = Die.query.count()

        self.assertEqual(set_counter, 1)
        self.assertEqual(dice_counter, 6)

        # try to create an already existing dice

        result = self.client.post('/sets', data=json.dumps(data), content_type='application/json')
        self.assertEqual(result.status_code, 409)
        self.assertDescription(result, "A DiceSet called {} already exists".format(data['name']))

    def test_get_all_sets(self):
        # return 204 beacuse no set exists
        result = self.client.get('/sets')
        self.assertStatus(result, 204)

        # create 2 new DiceSets
        data = {"name": "animal",
                "dice": [
                    ["bear", "cow", "elephant", "panda", "bull", "rhino"],
                    ["monkey", "bat", "lion", "tiger", "koala", "crocodile"],
                    ["whale", "penguin", "dolphin", "orca", "seahorses", "turtle"],
                    ["rabbit", "mouse", "cat", "chicken", "dog", "horse"],
                    ["fox", "squirrel", "frog", "butterfly", "donkey", "pork"],
                    ["eagle", "parrot", "rooster", "dragon", "sheep", "snake"]
                ]}

        result = self.client.post('/sets', data=json.dumps(data), content_type='application/json')
        self.assertStatus(result, 201)
        self.assertDescription(result, "DiceSet successfully added")

        data = {"name": "halloween",
                "dice": [
                    ["blood", "bones", "cauldron", "potion", "cobweb", "candies"],
                    ["frankenstein", "ghost", "mummy", "vampire", "werewolf", "zombie"],
                    ["cat", "executioner", "death", "witch", "skull", "spider"],
                    ["fear", "coffin", "pumpkin", "graveyard", "haunted", "noose"],
                    ["axe", "knife", "lollipop", "moon", "scythe", "hat"],
                    ["clown", "demon", "devil", "goblin", "owl", "troll"]
                ]}

        result = self.client.post('/sets', data=json.dumps(data), content_type='application/json')
        self.assertStatus(result, 201)
        self.assertDescription(result, "DiceSet successfully added")

        # return 200 and
        result = self.client.get('/sets')
        self.assertStatus(result, 200)
        expected_body = [{"id": 1, "name": "animal"}, {"id": 2, "name": "halloween"}]
        body = json.loads(result.get_data(as_text=True))
        self.assertEqual(expected_body, body)

    def test_get_set(self):
        # create new DiceSet
        data = {"name": "animal",
                "dice": [
                    ["bear", "cow", "elephant", "panda", "bull", "rhino"],
                    ["monkey", "bat", "lion", "tiger", "koala", "crocodile"],
                    ["whale", "penguin", "dolphin", "orca", "seahorses", "turtle"],
                    ["rabbit", "mouse", "cat", "chicken", "dog", "horse"],
                    ["fox", "squirrel", "frog", "butterfly", "donkey", "pork"],
                    ["eagle", "parrot", "rooster", "dragon", "sheep", "snake"]
                ]}

        result = self.client.post('/sets', data=json.dumps(data), content_type='application/json')
        self.assertStatus(result, 201)
        self.assertDescription(result, "DiceSet successfully added")

        # try to get a non-existing DiceSet
        result = self.client.get('/sets/126')
        self.assertStatus(result, 404)
        self.assertDescription(result, 'DiceSet not found')

        # get the previously created DiceSet
        result = self.client.get('/sets/1')
        self.assertStatus(result, 200)

        expected_body = {
            "id": 1,
            "name": "animal",
            "dice": [
                {
                    "number": 1,
                    "figures": ["bear", "cow", "elephant", "panda", "bull", "rhino"]
                },
                {
                    "number": 2,
                    "figures": ["monkey", "bat", "lion", "tiger", "koala", "crocodile"]
                },
                {
                    "number": 3,
                    "figures": ["whale", "penguin", "dolphin", "orca", "seahorses", "turtle"]
                },
                {
                    "number": 4,
                    "figures": ["rabbit", "mouse", "cat", "chicken", "dog", "horse"]
                },
                {
                    "number": 5,
                    "figures": ["fox", "squirrel", "frog", "butterfly", "donkey", "pork"]
                },
                {
                    "number": 6,
                    "figures": ["eagle", "parrot", "rooster", "dragon", "sheep", "snake"]
                }
            ]
        }
        body = json.loads(result.get_data(as_text=True))
        self.assertEqual(expected_body, body)

    def test_delete_set(self):
        # try to delete a non-existing DiceSet
        result = self.client.delete('/sets/126')
        self.assertStatus(result, 404)
        self.assertDescription(result, 'DiceSet not found')

        # create new DiceSet
        data = {"name": "animal",
                "dice": [
                    ["bear", "cow", "elephant", "panda", "bull", "rhino"],
                    ["monkey", "bat", "lion", "tiger", "koala", "crocodile"],
                    ["whale", "penguin", "dolphin", "orca", "seahorses", "turtle"],
                    ["rabbit", "mouse", "cat", "chicken", "dog", "horse"],
                    ["fox", "squirrel", "frog", "butterfly", "donkey", "pork"],
                    ["eagle", "parrot", "rooster", "dragon", "sheep", "snake"]
                ]}
        result = self.client.post('/sets', data=json.dumps(data), content_type='application/json')
        self.assertStatus(result, 201)
        self.assertDescription(result, "DiceSet successfully added")

        result = self.client.delete('/sets/1')
        self.assertStatus(result, 200)
        self.assertDescription(result, "DiceSet successfully deleted")

    def test_roll_set(self):
        # non-existing DiceSet
        result = self.client.post('/sets/1/roll', data=None)
        self.assert404(result)
        self.assertDescription(result, "DiceSet not found")

        # create new DiceSet
        data = {"name": "animal",
                "dice": [
                    ["bear", "cow", "elephant", "panda", "bull", "rhino"],
                    ["monkey", "bat", "lion", "tiger", "koala", "crocodile"],
                    ["whale", "penguin", "dolphin", "orca", "seahorses", "turtle"],
                    ["rabbit", "mouse", "cat", "chicken", "dog", "horse"],
                    ["fox", "squirrel", "frog", "butterfly", "donkey", "pork"],
                    ["eagle", "parrot", "rooster", "dragon", "sheep", "snake"]
                ]}
        result = self.client.post('/sets', data=json.dumps(data), content_type='application/json')
        self.assertStatus(result, 201)
        self.assertDescription(result, "DiceSet successfully added")

        # incorrect body (no JSON)
        result = self.client.post('/sets/1/roll', data=None)
        self.assert400(result)
        self.assertDescription(result, "Not valid request body")

        # no dice_number specified in request body
        result = self.client.post('/sets/1/roll', data=json.dumps({}), content_type='application/json')
        self.assert400(result)
        self.assertDescription(result, "Specify number of dice you want to roll")

        # invalid dice_number value
        # smaller than 2
        data = {'dice_number': 0}
        result = self.client.post('/sets/1/roll', data=json.dumps(data), content_type='application/json')
        self.assert400(result)
        self.assertDescription(result, "Number of dice to roll must be between 2 and 6")

        # bigger than 6
        data = {'dice_number': 126}
        result = self.client.post('/sets/1/roll', data=json.dumps(data), content_type='application/json')
        self.assert400(result)
        self.assertDescription(result, "Number of dice to roll must be between 2 and 6")

        # roll succesfully
        dice_number = 4
        data = {'dice_number': dice_number}
        result = self.client.post('/sets/1/roll', data=json.dumps(data), content_type='application/json')
        self.assert200(result)

        # check that body contains 5 keys (so 5 couple < number: figures >)
        body = json.loads(result.get_data(as_text=True))
        self.assertEqual(len(body), dice_number)

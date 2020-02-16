from flask import Flask
from sqlalchemy import func

from .database import db, DiceSet, Die
from .urls import DEFAULT_DB, TEST_DB
from .views import blueprints


def create_app(database=DEFAULT_DB, wtf=False):
    flask_app = Flask(__name__)
    flask_app.config['TESTING'] = (database == TEST_DB)
    flask_app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    flask_app.config['SECRET_KEY'] = 'ANOTHER ONE'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = database
    flask_app.config['WTF_CSRF_ENABLED'] = wtf

    for bp in blueprints:
        flask_app.register_blueprint(bp)
        bp.app = flask_app

    db.init_app(flask_app)
    db.create_all(app=flask_app)

    if database == DEFAULT_DB:
        with flask_app.app_context():
            # STANDARD SET
            if DiceSet.query.filter(func.lower(DiceSet.name) == 'standard').first() is None:
                standard = DiceSet()
                standard.id = 1
                standard.name = "standard"
                db.session.add(standard)
                db.session.commit()

                figures = [
                    ["bike", "moonandstars", "bag", "bird", "crying", "angry"],
                    ["tulip", "mouth", "caravan", "whale", "drink", "clock"],
                    ["happy", "coffee", "plate", "bus", "paws", "letter"],
                    ["cat", "pencil", "baloon", "bananas", "phone", "icecream"],
                    ["ladder", "car", "fir", "bang", "hat", "hamburger"],
                    ["rain", "heart", "glasses", "poo", "ball", "sun"]
                ]

                for i in range(6):
                    die = Die()
                    die.number = i + 1
                    die.id_set = 1
                    die.figures = '#' + '#'.join(figures[i]) + '#'
                    db.session.add(die)
                db.session.commit()

            # ANIMAL SET
            if DiceSet.query.filter(func.lower(DiceSet.name) == 'animal').first() is None:
                standard = DiceSet()
                standard.id = 2
                standard.name = "animal"
                db.session.add(standard)
                db.session.commit()

                figures = [
                    ["bear", "cow", "elephant", "panda", "bull", "rhino"],
                    ["monkey", "bat", "lion", "tiger", "koala", "crocodile"],
                    ["whale", "penguin", "dolphin", "orca", "seahorses", "turtle"],
                    ["rabbit", "mouse", "cat", "chicken", "dog", "horse"],
                    ["fox", "squirrel", "frog", "butterfly", "donkey", "pork"],
                    ["eagle", "parrot", "rooster", "dragon", "sheep", "snake"]
                ]

                for i in range(6):
                    die = Die()
                    die.number = i + 1
                    die.id_set = 2
                    die.figures = '#' + '#'.join(figures[i]) + '#'
                    db.session.add(die)
                db.session.commit()

            # HALLOWEEN SET
            if DiceSet.query.filter(func.lower(DiceSet.name) == 'halloween').first() is None:
                standard = DiceSet()
                standard.id = 3
                standard.name = "halloween"
                db.session.add(standard)
                db.session.commit()

                figures = [
                    ["blood", "bones", "cauldron", "potion", "cobweb", "candies"],
                    ["frankenstein", "ghost", "mummy", "vampire", "werewolf", "zombie"],
                    ["cat", "executioner", "death", "witch", "skull", "spider"],
                    ["fear", "coffin", "pumpkin", "graveyard", "haunted", "noose"],
                    ["axe", "knife", "lollipop", "moon", "scythe", "hat"],
                    ["clown", "demon", "devil", "goblin", "owl", "troll"]
                ]

                for i in range(6):
                    die = Die()
                    die.number = i + 1
                    die.id_set = 3
                    die.figures = '#' + '#'.join(figures[i]) + '#'
                    db.session.add(die)
                db.session.commit()

    return flask_app


app = create_app()

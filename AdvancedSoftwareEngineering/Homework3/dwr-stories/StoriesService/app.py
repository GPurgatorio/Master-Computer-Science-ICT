import datetime

from flask import Flask

from StoriesService.database import db, Story
from StoriesService.urls import DEFAULT_DB
from StoriesService.views import blueprints


def create_app(database=DEFAULT_DB, wtf=False, login_disabled=False):
    flask_app = Flask(__name__)
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    flask_app.config['SECRET_KEY'] = 'ANOTHER ONE'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = database
    flask_app.config['WTF_CSRF_ENABLED'] = wtf
    flask_app.config['LOGIN_DISABLED'] = login_disabled

    for bp in blueprints:
        flask_app.register_blueprint(bp)
        bp.app = flask_app

    db.init_app(flask_app)
    db.create_all(app=flask_app)

    return flask_app


app = create_app()
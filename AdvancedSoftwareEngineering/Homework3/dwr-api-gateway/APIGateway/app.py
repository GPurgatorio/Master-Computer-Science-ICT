from flask import Flask

from APIGateway.auth import login_manager
from APIGateway.urls import DEFAULT_DB
from APIGateway.views import blueprints


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

    login_manager.init_app(flask_app)

    return flask_app


app = create_app()

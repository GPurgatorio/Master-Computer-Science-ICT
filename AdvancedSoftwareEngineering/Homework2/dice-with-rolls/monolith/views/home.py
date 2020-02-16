from flask import Blueprint, render_template

from monolith.database import db, Story, Like
from monolith.auth import current_user


home = Blueprint('home', __name__)


def _strava_auth_url(config):
    return '127.0.0.1:5000'


@home.route('/')
def index():
    if current_user is not None and hasattr(current_user, 'id'):
        stories = db.session.query(Story).filter(Story.author_id == current_user.id)
    else:
        stories = None
    return render_template("index.html", stories=stories)

# Global URLS for extensibility
import os

from flask import flash, redirect, url_for

HOME_URL = 'http://127.0.0.1'
GATEWAY_URL = HOME_URL + ':5000/'

USER_PORT = ':5001'
DICE_PORT = ':5002'
STORY_PORT = ':5003'
REACTION_PORT = ':5004'

USER_URL = HOME_URL + USER_PORT
DICE_URL = HOME_URL + DICE_PORT
STORY_URL = HOME_URL + STORY_PORT
REACTION_URL = HOME_URL + REACTION_PORT


# Database in memory
TEST_DB = 'sqlite:///:memory:'

# Database "storytellers.db"
DEFAULT_DB = 'sqlite:///storytellers.db'

# Path where the .yaml file are
YML_PATH = os.path.join(os.path.dirname(__file__), 'yamls')


def check_service_up(response):
    if response.status_code == 500:
        flash('The requested microservice has encountered an Internal Server error.', 'error')
        return False
    return True


def service_not_up():
    flash('A requested microservice is not up', 'error')
    return redirect(url_for('gateway._home'))

import requests
from celery import Celery

from APIGateway.urls import HOME_URL, REACTION_PORT

_APP = None

BACKEND = BROKER = 'redis://localhost:6379'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)


@celery.task
def reaction_task(id_story, reaction_caption, id_user):
    data = {"story_id": id_story, "reaction_caption": reaction_caption, "current_user": id_user}

    x = requests.post(HOME_URL + REACTION_PORT + "/react", json=data)
    if x.status_code == 500:
        return None
    else:
        return (x.json())['description']

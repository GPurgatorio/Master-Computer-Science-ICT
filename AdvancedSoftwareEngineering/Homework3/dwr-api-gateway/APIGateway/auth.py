import functools

import requests
from flask_login import LoginManager, current_user

from APIGateway.classes.User import User
from APIGateway.urls import USER_URL, check_service_up

login_manager = LoginManager()


def admin_required(func):
    @functools.wraps(func)
    def _admin_required(*args, **kw):
        admin = current_user.is_authenticated and current_user.is_admin
        if not admin:
            return login_manager.unauthorized()
        return func(*args, **kw)
    return _admin_required


@login_manager.user_loader
def load_user(user_id):
    user = None
    x = requests.get(USER_URL + '/users/{}'.format(user_id))
    if check_service_up(x):
        body = x.json()
        if x.status_code < 300:
            user = User(body['id'], body['firstname'], body['lastname'], body['email'])
            user._authenticated = True
    return user

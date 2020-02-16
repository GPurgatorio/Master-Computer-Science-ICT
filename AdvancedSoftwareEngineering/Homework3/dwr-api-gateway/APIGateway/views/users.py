import requests
from flakon import SwaggerBlueprint
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from APIGateway.urls import *

usersapi = SwaggerBlueprint('users', '__name__', swagger_spec=os.path.join(YML_PATH, 'users-api.yaml'))


# Renders a page (users.html) with a list of all the users
@usersapi.operation('getAll')
def _get_all_users():
    try:
        x = requests.get(USER_URL + '/users')
    except requests.exceptions.ConnectionError:
        return service_not_up()
    users = []

    if check_service_up(x):
        users = x.json()

    return render_template("users.html", users=users, home_url=GATEWAY_URL)


# Renders a page (wall.html) with the wall of a specified user
@usersapi.operation('getUser')
def _get_user(id_user):
    try:
        u = requests.get(USER_URL + '/users/{}'.format(id_user))
    except requests.exceptions.ConnectionError:
        return service_not_up()

    if u.status_code < 300:
        user = u.json()
        try:
            fs = requests.get(USER_URL + '/users/{}/stats'.format(id_user))
            followers_stats = fs.json()
        except requests.exceptions.ConnectionError:
            return service_not_up()

        if fs.status_code < 300:
            try:
                ss = requests.get(STORY_URL + '/stories/stats/{}'.format(id_user))
            except requests.exceptions.ConnectionError:
                return service_not_up()
            if ss.status_code < 300:
                stories_stats = ss.json()
                try:
                    rs = requests.get(USER_URL + '/reactions/stats/user/{}'.format(id_user))
                except requests.exceptions.ConnectionError:
                    return service_not_up()
                if rs.status_code < 300:
                    reactions_stats = rs.json()
                else:
                    reactions_stats = {"tot_num_reactions": 0, "avg_reactions": 0.0}

                stats = {'follower_stats': followers_stats, 'stories_stats': stories_stats,
                         'reactions_stats': reactions_stats}
                if current_user is None or not hasattr(current_user, 'id'):
                    return render_template("wall.html", my_wall=False, not_foudn=False, user_info=user,
                                           stats=stats, home_url=GATEWAY_URL)
                return render_template("wall.html", my_wall=(current_user.id == user['id']), not_found=False,
                                       user_info=user, stats=stats, home_url=GATEWAY_URL)

        flash("Can't retrieve stories stats")
        return redirect(url_for('gateway._home'))
    else:
        return render_template("wall.html", not_found=True, home_url=GATEWAY_URL)


# The operation to follow a specific user
@usersapi.operation('followUser')
@login_required
def _follow_user(id_user):
    try:
        x = requests.post(USER_URL + '/users/{}/follow?current_user_id={}'.format(id_user, current_user.id))
    except requests.exceptions.ConnectionError:
        return service_not_up()
    if check_service_up(x):
        body = x.json()
        if x.status_code <= 500:
            flash(body['description'], 'error')

    return redirect(url_for('users._get_user', id_user=id_user))


# The operation to unfollow a specific user
@usersapi.operation('unfollowUser')
@login_required
def _unfollow_user(id_user):
    try:
        x = requests.post(USER_URL + '/users/{}/unfollow?current_user_id={}'.format(id_user, current_user.id))
    except requests.exceptions.ConnectionError:
        return service_not_up()

    if check_service_up(x):
        body = x.json()
        if x.status_code <= 500:
            flash(body['description'], 'error')

    return redirect(url_for('users._get_user', id_user=id_user))


# Get a list of all the followers of a specified user
@usersapi.operation('getFollowers')
def _get_followers(id_user):
    try:
        x = requests.get(USER_URL + '/users/' + id_user + '/followers')
    except requests.exceptions.ConnectionError:
        return service_not_up()
    followers = []

    if check_service_up(x):
        followers = x.json()

    return render_template("followers.html", users=followers, home_url=GATEWAY_URL)


# Get all the posted stories of a specified user
@usersapi.operation('getStoriesOfUser')
def _get_stories_of_user(id_user):
    try:
        s = requests.get(STORY_URL + '/stories/users/{}'.format(id_user))
    except requests.exceptions.ConnectionError:
        return service_not_up()
    stories = []
    if s.status_code < 300:
        stories = s.json()

    return render_template("user_stories.html", stories=stories, home_url=GATEWAY_URL)

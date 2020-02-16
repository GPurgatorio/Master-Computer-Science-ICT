import datetime
import os

from flakon import SwaggerBlueprint
from flask import jsonify, request, abort
from sqlalchemy import or_, and_

from UsersService.database import db, User, Follower

YML = os.path.join(os.path.dirname(__file__), '..', 'static', 'API_users.yaml')
users = SwaggerBlueprint('users', '__name__', swagger_spec=YML)


# Return the list of all users
@users.operation('getUsers')
def _users():
    usrs = db.session.query(User)
    return jsonify([user.serialize() for user in usrs])


# Create a new user
@users.operation('createUser')
def _create_user():
    try:
        user_data = request.get_json(request)
        print(user_data)

        # check user existence
        q = db.session.query(User).filter(User.email == user_data['email'])
        user = q.first()
        if user is not None:
            abort(406, 'The email address is already being used')
        # check date of birth < today
        dateofbirth = datetime.datetime.strptime(user_data['dateofbirth'], '%Y-%m-%d')
        if dateofbirth > datetime.datetime.today():
            abort(400, 'Date of birth can not be greater than today')

        # create new user
        new_user = User()
        new_user.firstname = user_data['firstname']
        new_user.lastname = user_data['lastname']
        new_user.email = user_data['email']
        new_user.dateofbirth = dateofbirth
        new_user.is_admin = False
        new_user.set_password(user_data['password'])
        db.session.add(new_user)
        db.session.commit()
    # If values in request body aren't well-formed
    except (ValueError, KeyError) as e:
        print(e)
        abort(400, 'Error with one parameter')

    return jsonify(description="New user created"), 201


# Check email and password of a user and return its id
@users.operation('loginUser')
def _login():
    try:
        user_data = request.get_json(request)

        # Check user existence
        q = db.session.query(User).filter(User.email == user_data['email'])
        user = q.first()
        if user is None:
            abort(404, 'The specified email does not exist')

        # Check password
        if not user.authenticate(user_data['password']):
            abort(400, 'Password uncorrect')

        # Return the user
        return jsonify(user.serialize()), 200

    except KeyError:
        abort(400, 'Error with one parameter')


# Return informations about a user
@users.operation('getUserData')
def _wall(userid):
    """ Ci pensa l'API gateway a differenziare tra my wall e other user wall,
         le informazioni vanno restituite tutte """
    q = db.session.query(User).filter(User.id == userid)
    user = q.first()

    # Check user existence
    if user is None:
        abort(404, 'The specified userid does not exist')
    # Return user wall
    else:
        return jsonify(user.serialize_all())


# Let a user follows another one
@users.operation('followUser')
def _follow_user(userid):
    current_user_id = None
    try:
        current_user_id = int(request.args.get('current_user_id'))
    # If values in request body aren't well-formed
    except ValueError:
        abort(400, "Error with current_user_id parameter")
    if current_user_id is None:
        abort(400, "Error with current_user_id parameter")

    # Check users existence
    if not _check_user_existence(userid):
        abort(404, 'The specified userid does not exist')
    if not _check_user_existence(current_user_id):
        abort(404, 'The specified current_user_id does not exist')
    # Check correctness
    if int(userid) == current_user_id:
        abort(400, "Can't follow yourself")
    if _check_follower_existence(current_user_id, userid):
        abort(400, "You already follow this storyteller")

    new_follower = Follower()
    new_follower.follower_id = current_user_id
    new_follower.followed_id = userid

    # Add follower to database
    db.session.add(new_follower)
    db.session.query(User).filter_by(id=userid).update({'follower_counter': User.follower_counter + 1})
    db.session.commit()

    return jsonify(description="User followed"), 200


# Let a user unfollows another one
@users.operation('unfollowUser')
def _unfollow_user(userid):
    current_user_id = None
    try:
        current_user_id = int(request.args.get('current_user_id'))
    # If values in request body aren't well-formed
    except Exception:
        abort(400, "Error with current_user_id parameter")
    if current_user_id is None:
        abort(400, "Error with current_user_id parameter")

    # Check user existence
    if not _check_user_existence(userid):
        abort(404, 'The specified userid does not exist')
    if not _check_user_existence(current_user_id):
        abort(404, 'The specified current_user_id does not exist')
    # Check correctness
    if int(userid) == current_user_id:
        abort(400, "You can't follow yourself")
    if not _check_follower_existence(current_user_id, userid):
        abort(400, "You should follow this storyteller before unfollowing")

    Follower.query.filter_by(follower_id=current_user_id, followed_id=userid).delete()
    db.session.query(User).filter_by(id=userid).update({'follower_counter': User.follower_counter - 1})
    db.session.commit()

    return jsonify(description="User unfollowed"), 200


# Return the list of users following the user identified by userid
@users.operation('getFollowers')
def _followers(userid):
    # Check user existence
    if not _check_user_existence(userid):
        abort(404, 'The specified userid does not exist')
    # Return followers list
    else:
        usrs = User.query.join(Follower, User.id == Follower.follower_id).filter_by(followed_id=userid)
        return jsonify([user.serialize() for user in usrs])

    # Return the statistics of a user


@users.operation('getUserStats')
def _user_stats(user_id):
    # Check user existence
    if not _check_user_existence(user_id):
        abort(404, 'The specified userid does not exist')
    # Return statistics
    else:
        num_followers = User.query.filter_by(id=user_id).first().follower_counter
        actual_month = datetime.date.today()
        first_day = actual_month.replace(day=1)
        this_month_follower = Follower.query.filter(
            and_(Follower.follower_id == user_id, Follower.creation_date >= first_day)).count()

        result = {
            "num_followers": num_followers,
            "followers_last_month": this_month_follower
        }

        return jsonify(result)

    # Return True if the user identified by userid exists


# Return the result of the search in the user list
@users.operation('search')
def _search():
    try:
        # Retrive parameter inserted in the search
        query = request.args.get('query')

        # If it is None return Error, otherwise delete withespace in the string
        if query is None:
            abort(400, 'Error with query parameter')
        else:
            query = query.strip()

        usrs = []

        # Check if there are user with the specified name or surname
        if query != '':
            usrs = User.query.filter(
                or_(User.firstname.like('%' + query + '%'), User.lastname.like('%' + query + '%'))).all()

        # Return the result of the search
        if len(usrs) > 0:
            return jsonify([user.serialize() for user in usrs])
        else:
            return jsonify({}), 204
            # If values in request body aren't well-formed
    except ValueError:
        abort(400, 'Error with query parameter')


def _check_user_existence(userid):
    user = db.session.query(User).filter(User.id == userid)
    return user.first() is not None


# Return True if the user identified by follower_id follows the user identified by followed_id
def _check_follower_existence(follower_id, followed_id):
    follower = db.session.query(Follower).filter_by(follower_id=follower_id, followed_id=followed_id)
    return follower.first() is not None

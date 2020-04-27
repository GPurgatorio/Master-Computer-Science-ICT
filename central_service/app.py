#!flask/bin/python
from flask import Flask, request, jsonify, session, render_template, redirect, url_for, flash
from flask_pymongo import PyMongo
import bcrypt

''' If we want to be secure
secrets = open("super_secret.txt", "r")
secrets_splitted = secrets.read().split()
mongodb_pass = secrets_splitted[0]
session_secret = secrets_splitted[1]
'''
#else
mongodb_pass = "chessarmi"
session_secret = "mysecret"

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://chessarmi:"+mongodb_pass + \
	"@mcps-project-txguh.mongodb.net/chessaRMI?retryWrites=true&w=majority"

mongo = PyMongo(app)


def is_logged(session):
	return 'name' in session and 'surname' in session


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    if is_logged(session):
        return render_template("user.html", name=session['name'], surname=session['surname'])

    return render_template("login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        login_user = mongo.db.users.find_one({'email': form['inputEmail']})

        if login_user:
            if bcrypt.hashpw(form['inputPassword'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['is_logged'] = True
                session['email'] = login_user['email']
                session['name'] = login_user['name']
                session['surname'] = login_user['surname']
                return render_template("user.html", name=session['name'], surname=session['surname'])

        flash('Wrong credentials')
        return render_template("login.html")

    if request.method == 'GET':
        return redirect(url_for("home"))


@app.route('/logout', methods=['GET'])
def logout():
    # [session.pop(key) for key in list(session.keys()) if key != '_flashes']   <- can be used if flash msgs are needed
    session.clear()
    return redirect(url_for("home"))

#
# MOCK endpoints. Administrators stuff. Only with PostMan
#


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Use Postman!
    if request.method == 'POST':
        json_request = request.get_json()
        users = mongo.db.users
        existing_user = users.find_one({'email': json_request['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                json_request['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'email': json_request['email'],
                          'password': hashpass,
                          'name': json_request['name'],
                          'surname': json_request['surname'],
                          'face_code': json_request['face_code'],
                          "rooms" : []
                          })
            return "OK!", 201

        return 'That username already exists!', 400

    if request.method == 'GET':
        # render template register
        return "To do (maybe)", 200


@app.route('/api/v0.0/users', methods=['GET'])
def users():
    users_to_return = []
    for user in mongo.db.users.find():
        user['_id'] = str(user['_id'])
        user['password'] = str(user['password'])
        users_to_return.append(user)
    return jsonify(users_to_return), 200


@app.route('/api/v0.0/users/<id>', methods=['GET'])
def users_id(id):
    user_to_return = mongo.db.users.find_one_or_404({"_id": id})
    return jsonify(user_to_return), 200


@app.route('/api/v0.0/rooms', methods=['GET', 'POST', 'PUT'])
def rooms():
    rooms_to_return = []
    for room in mongo.db.rooms.find():
        room['_id'] = str(room['_id'])
        rooms_to_return.append(room)
    return jsonify(rooms_to_return), 200


@app.route('/api/v0.0/rooms/<id>', methods=['GET'])
def room_id(id):
    room_to_return = mongo.db.rooms.find_one_or_404({"_id": id})
    return jsonify(room_to_return), 200

@app.route('/api/v0.0/rooms/new', methods=['POST'])
def room_new():
    json_request = request.get_json()
    mongo.db.rooms.insert({'name': json_request['name'], "users_allowed" : []})
    return "OK!", 201

@app.route('/api/v0.0/policies', methods=['GET', 'POST', 'PUT'])
def policies():
    policies_to_return = []
    for policy in mongo.db.policies.find():
        policy['_id'] = str(policy['_id'])
        policies_to_return.append(policy)
    return jsonify(policies_to_return), 200


@app.route('/api/v0.0/policies/<id>', methods=['GET'])
def policy_id(id):
    policy_to_return = mongo.db.policies.find_one_or_404({"_id": id})
    return jsonify(policy_to_return), 200


@app.route('/api/v0.0/policies/new', methods=['GET', 'POST'])
def boffa():
    json_request = request.get_json()
    user_for_policie = mongo.db.users.find_one_or_404({"email": json_request["email"]})
    room_for_policie = mongo.db.rooms.find_one_or_404({"name": json_request["room_name"]})
    if request.method == 'POST':
        policies = mongo.db.policies
        policies.insert(
            {
                "user_id": user_for_policie["_id"],
                "room_id": room_for_policie["_id"]
            }
        )
        mongo.db.users.update_one({"_id" : user_for_policie["_id"]}, {'$push': {'rooms': room_for_policie["_id"]}})
        mongo.db.rooms.update_one({"_id" : room_for_policie["_id"]}, {'$push': {'users_allowed': user_for_policie["_id"]}})

    return "OK!", 201

if __name__ == '__main__':
    app.secret_key = session_secret
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run(debug=True)

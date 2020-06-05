#!flask/bin/python
import json
import threading

import bcrypt
import paho.mqtt.client as mqtt
from flask import Flask, request, jsonify, session, render_template, redirect, url_for, flash
from flask_pymongo import PyMongo

from config import *
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = DB_URL

mongo = PyMongo(app)


def is_logged(session):
    return 'name' in session and 'surname' in session


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    if is_logged(session):
        login_user = mongo.db.users.find_one({'email': session['email']})
        policies_to_return = get_policies(login_user["_id"])
        return render_template("user.html", name=session['name'], surname=session['surname'],
                               policies=policies_to_return, admin=session['admin'])

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
                session['admin'] = login_user['admin']
                policies_to_return = get_policies(login_user["_id"])

                return render_template("user.html", name=session['name'], surname=session['surname'],
                                       policies=policies_to_return, admin=session['admin'])

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
            users.insert_one({'email': json_request['email'],
                              'password': hashpass,
                              'name': json_request['name'],
                              'surname': json_request['surname'],
                              'face_code': json_request['face_code'],
                              'rooms': [],
                              'devices_id': [],
                              'admin': False
                              })
            return "OK!", 201

        return 'That username already exists!', 400

    if request.method == 'GET':
        # render template register
        return "To do (maybe)", 200


@app.route('/users/new_photo', methods=['POST'])
def new_photo():
    # Use Postman!
    if request.method == 'POST':
        json_request = request.get_json()
        users = mongo.db.users
        existing_user = users.find_one({'email': json_request['email']})

        if existing_user is not None:

            mongo.db.users.update_one({"_id": existing_user["_id"]},  { '$set' :{
                                      'face_code': json_request['face_code']}})

            return "OK!", 201

        return 'That username does not exists!', 400


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
    mongo.db.rooms.insert_one(
        {'name': json_request['name'], "users_allowed": []})
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


@app.route("/policy/new")
def add_policy():
    if not is_logged(session):
        flash("Login first")
        return redirect(url_for("home"))

    if not session['admin']:
        flash("You must be an admin to add policies")
        return redirect(url_for("home"))

    users_to_return = []
    rooms_to_return = []
    policies_to_return = []
    for room in mongo.db.rooms.find():
        room['_id'] = str(room['_id'])
        rooms_to_return.append(room)

    for user in mongo.db.users.find():
        user['_id'] = str(user['_id'])
        users_to_return.append(user)

    tot = 1     # num of policies (0 FR, 1 BT + FR)
    for policy in mongo.db.policies.find():
        if int(policy['type']) > tot:
            tot = policy['type']

    for i in range(tot+1):
        policies_to_return.append({"type": str(i)})

    return render_template("add_policy.html", users=users_to_return, rooms=rooms_to_return, policies=policies_to_return,
                           admin=session['admin'])


@app.route('/api/v0.0/policies/new', methods=['POST'])
def boffa():
    form = request.form
    user_for_policy = mongo.db.users.find_one_or_404({"email": form["email"]})
    room_for_policy = mongo.db.rooms.find_one_or_404(
        {"name": form["room_name"]})
    if request.method == 'POST' and is_logged(session):
        check = mongo.db.policies.find({"user_id": ObjectId(
            user_for_policy["_id"]), "room_id": ObjectId(room_for_policy["_id"])})

        if check.count():
            flash("Already existing policy")
            return redirect(url_for("add_policy"))

        policies = mongo.db.policies
        policies.insert_one(
            {
                "user_id": user_for_policy["_id"],
                "room_id": room_for_policy["_id"],
                "type": int(form["plc"])
            }
        )
        mongo.db.users.update_one({"_id": user_for_policy["_id"]}, {
                                  '$push': {'rooms': room_for_policy["_id"]}})
        mongo.db.rooms.update_one({"_id": room_for_policy["_id"]},
                                  {'$push': {'users_allowed': user_for_policy["_id"]}})

        flash("Policy added correctly")
        return redirect(url_for("add_policy"))

    flash("It either wasn't a POST or you're not logged in")
    return redirect(url_for("home"))


# Auxiliary functions

def get_policies(_id):
    # Returns the policies for the given user_id for each room he's "in"
    policies_to_return = []
    for policy in mongo.db.policies.find():
        if not _id == policy["user_id"]:
            continue
        give_me_a_policy_list = policies_to_str(policy)
        if give_me_a_policy_list is None:
            continue
        policies_to_return.append(give_me_a_policy_list)
    return policies_to_return


# Writes the policies in string format depending on the "type" field
def policies_to_str(policy):
    r = mongo.db.rooms.find_one({'_id': policy["room_id"]})
    if not r:
        return None
    res = {}
    if policy["type"] == 0:
        res = {"room": r["name"], "name": "Face Recognition"}
    elif policy["type"] == 1:
        res = {"room": r["name"], "name": "Face Recognition + Bluetooth"}
    return res


def insert_in_mongo_thread(msg):
    mongo.db.discovered_devices.insert_one(msg)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(REQUEST_TOPIC)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    th = threading.Thread(target=insert_in_mongo_thread,
                          args=(json.loads(msg.payload),))
    th.daemon = True
    th.start()


client = mqtt.Client()

if __name__ == '__main__':
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
    client.connect(MQTT_ADDRESS, MQTT_PORT, 5)
    client.loop_start()

    app.secret_key = SESSION_SECRET
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run(debug=True)

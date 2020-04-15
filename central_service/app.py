#!flask/bin/python
from flask import Flask, request, jsonify, session
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/chessaRMI"
mongo = PyMongo(app)


@app.route('/api/v0.0/users', methods=['GET'])
def users():
    users_to_return = []
    for user in mongo.db.users.find():
        users_to_return.append(user)
    return jsonify(users_to_return), 200


@app.route('/api/v0.0/users/<id>', methods=['GET'])
def users_id(id):
    user_to_return = mongo.db.users.find_one_or_404({"_id": id})
    return jsonify(user_to_return), 200


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    if 'name' in session and 'surname' in session:
        return 'You are logged in as ' + session['name'] + ' ' + session['surname'] , 200

    return 'You are not logged in', 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        json_request = request.get_json()
        users = mongo.db.users
        login_user = users.find_one({'email': json_request['email']})

        if login_user:
            if bcrypt.hashpw(json_request['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['is_logged'] = True
                session['email'] = login_user['email']
                session['name'] = login_user['name']
                session['surname'] = login_user['surname']
                return "OK!", 200

        return 'Invalid username/password combination', 400
    if request.method == 'GET':
        #rendetemplate login

@app.route('/register', methods=['GET','POST'])
def register():
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
                          'hash_faces': 0
                          })
            return "OK!", 201

        return 'That username already exists!', 400

    if request.method == 'GET':
        #rendetemplate register


@app.route('/api/v0.0/rooms', methods=['GET', 'POST', 'PUT'])
def rooms():
    rooms_to_return = []
    for room in mongo.db.rooms.find():
        rooms_to_return.append(room)
    return jsonify(rooms_to_return), 200

@app.route('/api/v0.0/rooms/<id>', methods=['GET'])
def room_id(id):
    room_to_return = mongo.db.rooms.find_one_or_404({"_id": id})
    return jsonify(room_to_return), 200

@app.route('/api/v0.0/policies', methods=['GET', 'POST', 'PUT'])
def policies():
    policies_to_return = []
    for policy in mongo.db.policies.find():
        policies_to_return.append(policy)
    return jsonify(policies_to_return), 200

@app.route('/api/v0.0/policies/<id>', methods=['GET'])
def policy_id(id):
    policy_to_return = mongo.db.policies.find_one_or_404({"_id": id})
    return jsonify(policy_to_return), 200

@app.route('/api/v0.0/policies/new', methods=['GET','POST'])
    if request.method == 'GET':
        #rendetemplate
    
    if request.method == 'POST':
        #user must be logged in
        if 'email' in session:
            policies = mongo.db.policies
            policies.insert(
                {
                    "user_id": request.form['user_id'],
                    "room_id": request.form['room_id'],
                }
            )
        else:
            #redirect login
            
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
    
#!flask/bin/python
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/chessaRMI"
mongo = PyMongo(app)

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return "Hello World!"

@app.route('/api/v0.0/users', methods=['GET', 'POST', 'PUT'])
def users():
    #Test
    users = mongo.db.users.find().count()
    return jsonify("Users now in the db: " + str(users)), 200

@app.route('/api/v0.0/rooms', methods=['GET', 'POST', 'PUT'])
def rooms():
    return jsonify("rooms"), 200

@app.route('/api/v0.0/policies', methods=['GET', 'POST', 'PUT'])
def policies():
    return jsonify("policies"), 200

if __name__ == '__main__':
    app.run(debug=True)
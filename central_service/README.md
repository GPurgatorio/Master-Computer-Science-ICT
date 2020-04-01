
# How to install Central Service - Linux  

- Create a venv 
  - ```mkdir venv```
  - ```python3 -m venv ./venv```
- Activate the venv 
  - ```source ./venv/bin/activate```
- Install requirements
  - upgrade pip -> ```pip install --upgrade pip```
  - ```pip install -r requirements.txt```
- Start the app
  - ```chmod +x app.py```
  - ```./app.py```

You should already have Mongo DB server running in localhost port 27017
To install MongoDB (from [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#run-mongodb-community-edition)): 
- ```wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -```
- ```echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list```
- ```sudo apt-get update```
- ```sudo apt-get install -y mongodb-org```

And then to start it: 
- ```sudo systemctl start mongod```

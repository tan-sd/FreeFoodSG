from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import os, sys
import haversine as hs
import requests
import bcrypt
import json
# import re
# from invokes import invoke_http

# request.args for get param
# request.form for post param
# request.values for the abv 2

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True

if os.name == 'nt':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user_info'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/user_info'

db = SQLAlchemy(app)
CORS(app)

class User(db.Model):
    __tablename__ = 'user_info'

# for ref if want to change the format in sqlworkbench
# https://stackoverflow.com/questions/17371639/how-to-store-arrays-in-mysql

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.VARCHAR(64), nullable=False)
    last_name = db.Column(db.VARCHAR(64), nullable=False)
    username = db.Column(db.VARCHAR(64), nullable=False)
    number = db.Column(db.VARCHAR(12), nullable=False)
    email = db.Column(db.VARCHAR(128), nullable=False)
    password = db.Column(db.VARCHAR(64), nullable=False)
    address = db.Column(db.VARCHAR(128), nullable=False)
    latitude = db.Column(db.Float(precision=6), nullable=False)
    longitude = db.Column(db.Float(precision=6), nullable=False)
    dietary_type = db.Column(db.VARCHAR(64))
    travel_appetite = db.Column(db.Integer)
    sms_notif = db.Column(db.Integer())
    email_notif = db.Column(db.Integer())


    def __init__(self, user_id, first_name, last_name, username, number, email, password, address, latitude, longitude, dietary_type, travel_appetite, sms_notif, email_notif):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.number = number
        self.email = email
        self.password = password
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.dietary_type = dietary_type
        self.travel_appetite = travel_appetite
        self.sms_notif = sms_notif
        self.email_notif = email_notif

    def json(self):
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "number": self.number,
            "email": self.email,
            "password": self.password,
            "address": self.address,
            "latitude": self.latitude,
            "longitude":self.longitude,
            "dietary_type": self.dietary_type,
            "travel_appetite": self.travel_appetite,
            "sms_notif": self.sms_notif,
            "email_notif": self.email_notif
        }

    def get_distance(self, Location):
        '''
        input: Location

        syntax: self.get_distance(Location)

        output: Location JSON if Location within self.travel_appetite else Failure message
        '''
        distance = hs.haversine((self.latitude,self.longitude),(Location.latitude, Location.longitude))
        if distance <= self.travel_appetite:
            return {"post_id": Location.post_id, "address": Location.address, "latitude": Location.latitude, "longitude": Location.longitude}
        else:
            return "Method failed because distance larger than travel_appetite"

    
'''CREATE USER PROFILE
this function create a user account
input: updated full JSON of new user details, it must have:

{
    "user_id": 4,
    "first_name": "rach",
    "last_name": "sng",
    "username": "rachel",
    "number": 99999999,
    "email": "email",
    "password": "password",
    "address": "Victoria Street, Singapore Management University, Singapore",
    "latitude": 1.296273,
    "longitude": 103.850158,
    "dietary_type": [],
    "travel_appetite": 0.5,
    "sms_notif": 1,
    "email_notif": 1
}

output: 

{
    "code": 201,
    "data": {
        "address": "Victoria Street, Singapore Management University, Singapore",
        "dietary_type": "",
        "email": "email",
        "email_notif": 1,
        "first_name": "rach",
        "last_name": "sng",
        "latitude": 1.296273,
        "longitude": 103.850158,
        "number": "99999999",
        "password": "$2b$10$2xr3mD4TBX0gHAdHvagEFeQlv87YzjNDEvZ7ZqfUSpdWL3.R6JOiC",
        "sms_notif": 1,
        "travel_appetite": 1,
        "user_id": 11,
        "username": "rachel"
    },
    "message": "User created successfully."
}

'''

# to create user info when user first created account
@app.route("/user/<string:username>", methods=['POST'])
def create_user(username):
    print(username)

    new_user = User.query.filter_by(username=username).first()
    print(new_user)

    if (User.query.filter_by(username=username).first()):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "name": username
                },
                "message": "User already exist."
            }
        ), 404
    # 400 BAD request

    print('user dont exist so come over here')
    # store to db
    data = request.get_json()
    print(data)
    data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt(10))
    data['password'] = data['password'].decode('utf-8')
    data['dietary_type'] = ','.join(data['dietary_type'])
    user_id = User.query.order_by(User.user_id.desc()).first().user_id
    print(user_id)
    data['user_id'] = user_id + 1

    new_user = User(**data)
    print(new_user)
    print(data['dietary_type'])

    print(data['password'])
    print(data)


    try:
        print('in try loop')
        db.session.add(new_user)
        db.session.commit()
        # to commit the change
        return jsonify(
            {
                "code": 201,
                "data": new_user.json(),
                "message": "User created successfully."
            }
        ), 201
    except:
        print('in except')
        return jsonify(
            {
                "code": 500,
                "data": {
                    "name": username
                },
                "message": "An error occured creating the user."
            }
        ), 500
    

'''LOGS INTO USER ACCOUNT
this function checks user's username and password
input: updated full JSON of new user details, it must have:

{

    "username": "rachel",
    "password": "password"

}

output: 

{
    "code": 201,
    "msg": "Login Successfully",
    "user": {
        "address": "Victoria Street, Singapore Management University, Singapore",
        "dietary_type": "",
        "email": "email",
        "email_notif": 1,
        "first_name": "rach",
        "last_name": "sng",
        "latitude": 1.296273,
        "longitude": 103.850158,
        "number": "99999999",
        "sms_notif": 1,
        "travel_appetite": 1,
        "user_id": 11,
        "username": "rachel"
    }
}

'''
# let user log in 
@app.route("/login", methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()

    print(user)
    print(username)
    print(password)

    if user == None:
        print("[LOGIN] User signed in with wrong username or password.")
        return jsonify({
            "code": 404,
            "msg": "Username or password is wrong",
        }), 404
    
    elif user.username == username and (bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))):
    # elif user.username == username and user.password == password:# <-- ADAM - Uncomment this to test website w/o encryption
        user_info_return = user.json()
        del user_info_return['password']

        print("[LOGIN] User logged in successfully.")
        return jsonify({
            "code": 201,
            "msg": "Login Successfully",
            "user": user_info_return
        }), 201
    else:
        print("[LOGIN] User signed in with wrong username or password.")
        return jsonify({
            "code": 404,
            "msg": "Username or password is wrong",
        }), 404


'''SHOW ALL USERS ACCOUNT
this function returns all user profiles
input: nothing

output: 

{
    "code": 200,
    "data": {
        "user": [info.json() for info in all_user_info]
    }
}

which is 

{
    "code": 200,
    "data": {
        "user": [
            {
                "address": "Victoria Street, Singapore Management University, Singapore",
                "dietary_type": "",
                "email": "shengdatan@gmail.com",
                "email_notif": 1,
                "first_name": "Sheng Da",
                "last_name": "Tan",
                "latitude": 1.296273,
                "longitude": 103.850158,
                "number": "92476862",
                "password": "$2b$10$efG2mz/MMdwXckfqkcQph.l5cB.SzTkUdzuw/Sbe.kHcrHe1.0BG2",
                "sms_notif": 1,
                "travel_appetite": 1,
                "user_id": 9,
                "username": "shengdatan"
            },
            {
                "address": "Expo Drive, Singapore Expo, Singapore",
                "dietary_type": "Halal",
                "email": "adamft.2021@scis.smu.edu.sg",
                "email_notif": 1,
                "first_name": "Adam",
                "last_name": "Tan",
                "latitude": 1.333525,
                "longitude": 103.959537,
                "number": "92354902",
                "password": "$2b$10$BZK3ZvadKLLcOkRoaEr5ouFB8qu3ZpyaXUyCFjJd9MVkNWzSd6uOG",
                "sms_notif": 1,
                "travel_appetite": 2,
                "user_id": 10,
                "username": "adamtan"
            },
            {
                "address": "Victoria Street, Singapore Management University, Singapore",
                "dietary_type": "",
                "email": "email",
                "email_notif": 1,
                "first_name": "rach",
                "last_name": "sng",
                "latitude": 1.296273,
                "longitude": 103.850158,
                "number": "99999999",
                "password": "$2b$10$2xr3mD4TBX0gHAdHvagEFeQlv87YzjNDEvZ7ZqfUSpdWL3.R6JOiC",
                "sms_notif": 1,
                "travel_appetite": 1,
                "user_id": 11,
                "username": "rachel"
            }
        ]
    }
}

'''
# to diplay profile of all users
@app.route("/users", methods=['GET'])
def getUserInfo():
    all_user_info = User.query.all()
    if len(all_user_info):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "user": [info.json() for info in all_user_info]
                }
            }
        )
        
    # if HTTP status code not specified at the end, 
    # then 200 OK returned

    # else comes here
    return jsonify(
        {
            "code": 404,
            "message": "No information to be displayed."
        }
    ), 404   


'''DISPLAY USER PROFILE DETAILS
this function checks user's username 
input: it must have:

{
    "username": 'rachel', 
}

output: 

{
    "code": 200,
    "data": {
        "address": "Victoria Street, Singapore Management University, Singapore",
        "dietary_type": "",
        "email": "email",
        "email_notif": 1,
        "first_name": "rach",
        "last_name": "sng",
        "latitude": 1.296273,
        "longitude": 103.850158,
        "number": "99999999",
        "password": "$2b$10$2xr3mD4TBX0gHAdHvagEFeQlv87YzjNDEvZ7ZqfUSpdWL3.R6JOiC",
        "sms_notif": 1,
        "travel_appetite": 1,
        "user_id": 11,
        "username": "rachel"
    }
}

'''
# to display user info
@app.route("/profile/<string:username>", methods=['GET'])
def find_user(username):

    # shd display user profile
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404


'''EDIT USER PROFILE
this function edits user details, username stays the same
input: it must have:
{
    "code": 200,
    "data": {
        "address": "Victoria Street, Singapore Management University, Singapore",
        "dietary_type": "",
        "email": "newemail",
        "email_notif": 1,
        "first_name": "rach",   
        "last_name": "sng",
        "latitude": 1.296273,
        "longitude": 103.850158,
        "number": "99999999",
        "password": "$2b$10$2xr3mD4TBX0gHAdHvagEFeQlv87YzjNDEvZ7ZqfUSpdWL3.R6JOiC",
        "sms_notif": 1,
        "travel_appetite": 1,
        "user_id": 11,
        "username": "rachel"
    }
}

output: 

{
    "code": 200,
    "data": {
        "address": "Victoria Street, Singapore Management University, Singapore",
        "dietary_type": "",
        "email": "newemail",
        "email_notif": 1,
        "first_name": "rach",
        "last_name": "sng",
        "latitude": 1.296273,
        "longitude": 103.850158,
        "number": "99999999",
        "password": "$2b$10$2xr3mD4TBX0gHAdHvagEFeQlv87YzjNDEvZ7ZqfUSpdWL3.R6JOiC",
        "sms_notif": 1,
        "travel_appetite": 1,
        "user_id": 11,
        "username": "rachel"
    }
}

'''

# just to update user profile, according to the data receieved from website
@app.route("/profile/update", methods=['PUT'])
def update_by_user_id():

    print("editing profile...")
    

    if request.get_json():
        data = request.get_json()['data']
        print(data)
        username = data['username']
        user = User.query.filter_by(username=username).first()
        password = user.password

        if username:

            try: 
            
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.number = data['number']
                user.email = data['email']
                user.password = password
                user.address = data['address']
                user.latitude = data['latitude']
                user.longitude = data['longitude']
                user.dietary_type = data['dietary_type']
                user.travel_appetite = data['travel_appetite']
                user.sms_notif = data['sms_notif']
                user.email_notif = data['email_notif']
                db.session.commit()

                print('User details updated successfully')
                return jsonify(
                    {
                        "code": 200,
                        "data": user.json()
                    }
                )
        
            except Exception as e:
                print("Error occured while updating the post.")
                return jsonify(
                    {
                        "code": 500,
                        "data": {
                            "username": username
                        },
                        "message": "An error occurred while updating the post. System Message: " + str(e)
                    }
                ), 500
        # user not found
        return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
        ), 404
        
    
    return jsonify(
        {
            "code": 404,
            "message": "No data retrieved."
        }
    ), 404


'''
Details for wrapper function below

Function: search for users where the food post latlng is within the users' travel appetite
Input: 

{
    "latitude": 1.296568,
    "longitude": 103.852119
}

Output: 

{
    "code": 200,
    "data": {
        "user": [
            {
                "address": "Victoria Street, Singapore Management University, Singapore",
                "dietary_type": "",
                "email": "shengdatan@gmail.com",
                "email_notif": 1,
                "first_name": "Sheng Da",
                "last_name": "Tan",
                "latitude": 1.296273,
                "longitude": 103.850158,
                "number": "92476862",
                "password": "$2b$10$efG2mz/MMdwXckfqkcQph.l5cB.SzTkUdzuw/Sbe.kHcrHe1.0BG2",
                "sms_notif": 1,
                "travel_appetite": 1,
                "user_id": 9,
                "username": "shengdatan"
            },
            {
                "address": "Expo Drive, Singapore Expo, Singapore",
                "dietary_type": "Halal",
                "email": "adamft.2021@scis.smu.edu.sg",
                "email_notif": 1,
                "first_name": "Adam",
                "last_name": "Tan",
                "latitude": 1.333525,
                "longitude": 103.959537,
                "number": "92354902",
                "password": "$2b$10$BZK3ZvadKLLcOkRoaEr5ouFB8qu3ZpyaXUyCFjJd9MVkNWzSd6uOG",
                "sms_notif": 1,
                "travel_appetite": 2,
                "user_id": 10,
                "username": "adamtan"
            },
            {
                "address": "Victoria Street, Singapore Management University, Singapore",
                "dietary_type": "",
                "email": "newemail",
                "email_notif": 1,
                "first_name": "rach",
                "last_name": "sng",
                "latitude": 1.296273,
                "longitude": 103.850158,
                "number": "99999999",
                "password": "$2b$10$2xr3mD4TBX0gHAdHvagEFeQlv87YzjNDEvZ7ZqfUSpdWL3.R6JOiC",
                "sms_notif": 1,
                "travel_appetite": 1,
                "user_id": 11,
                "username": "rachel"
            }
        ]
    }
}

'''
@app.route("/filter_user", methods=['GET'])
# search for users that are within the distance
def filter_user():
    # check input format and data is JSON
    if request.method =='GET':
        # try:
            # get query info
            data = request.get_json()
            form_latitude = data['latitude']
            form_longitude = data['longitude']
            print("\nReceived lat & long from the form:")

            # do the actual checking
            # return list of user objects from userdB
            all_user_info = User.query.all()
            filtered_users = []
            if len(all_user_info):

                # filter for users who are "close" to post according to their travel appetite
                for user in all_user_info:
                    user_latitude = user.latitude
                    user_longitude = user.longitude
                    user_travel_appetite = float(user.travel_appetite)
                    query_latitude = float(form_latitude)
                    query_longitude = float(form_longitude)
                    distance = hs.haversine((user_latitude,user_longitude),(query_latitude, query_longitude))

                    if distance <= user_travel_appetite or distance >= user_travel_appetite:
                        filtered_users.append(user)

                # return list of user objects where the post is within the user's travel appetite
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "user": [info.json() for info in filtered_users]
                        }
                    }
                )
                          
            else:
                # the else comes here
                return jsonify(
                    {
                        "code": 404,
                        "message": "No information to be displayed."
                    }
                ), 404

if __name__ == '__main__':
    app.run(port=1111, debug=True)

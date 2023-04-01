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
        
@app.route('/')
def nothing():
    return 'user homepage'
    # return render_template('register.html')
    

# to create user info when user first created account
@app.route("/user/<string:username>", methods=['GET','POST'])
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
    
    # return jsonify(
    #     {
    #         "code": 201,
    #         "data": name
    #     }
    # ), 201
    
# let user log in 
@app.route("/login", methods=['POST', 'GET'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()

    print(user)
    print(username)
    print(password)

    # print(user.password)
    if user == None:
        print("[LOGIN] User signed in with wrong username or password.")
        return jsonify({
            "code": 404,
            "msg": "Username or password is wrong",
        }), 404
    
    # elif user.username == username and (bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))):
    elif user.username == username and user.password == password:# <-- ADAM - Uncomment this to test website w/o encryption
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

# to diplay profile of all users
@app.route("/users")
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

# to display user info
@app.route("/profile/<string:name>", methods=['GET'])
def find_user(name):

    # shd display user profile
    user = User.query.filter_by(name=name).first()
    if user:
        return jsonify(
            {
                "code": 200,
                "data": user
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404

# just to update user profile, according to the data receieved from website
@app.route("/profile/<string:name>/update", methods=['PUT'])
def update_by_user_id(name):
    
    user = User.query.filter_by(name=name).first()
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


'''
Details for wrapper function below

Function: search for users where the food post latlng is within the users' travel appetite
Input: food post JSON object
Output: array of user JSON objects who fulfill the criteria
'''
@app.route("/filter_user", methods=['POST'])
# search for users that are within the distance
def filter_user():
    # check input format and data is JSON
    if request.method =='POST':
        # try:
            # get query info
            data = request.get_json()
            form_latitude = data.latitude
            form_longitude = data.longitude
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


# # user create account
# @app.route("/register", methods=['POST', 'GET'])
# def register_user():

#     if request.method =='POST':
#         status = False
#         error_msg = ''
#         username = request.form.get('username')
#         name = request.form.get('name')
#         password = request.form.get('password')
#         dietary = request.form.get('dietary')
#         travel_appetite = request.form.get('travel_appetite')
#         default_address = request.form.get('default_address')

#         # check if user name exists
        # if user_info.query.filter_by(username=username).first():
        #     error_msg += 'user alr exists'

        # # here will have all the checking done.
        # if (len(password)<=11):
        #     error_msg += 'min length 12'
        #     # return render_template('register_fail.html', msg = error_msg)
            
        # if not re.search("[a-z]", password):
        #     error_msg += '\n need at least 1 small alphabet'
        #     # return render_template('register_fail.html', msg = error_msg)
     
        # # elif not re.search("[A-Z]", password):
     
        # if not re.search("[0-9]", password):
        #     error_msg += '\n need min 1 number'
        #     # return render_template('register_fail.html', msg = error_msg)
      
        # if not re.search("[_@$]" , password):
        #     error_msg += '\n need min 1 symbol'
            # return render_template('register_fail.html', msg = error_msg)
    
        # elif re.search("\s" , password):
        #     error_msg = 'min length 12'
        #     return render_template('register_fail.html', msg = error_msg)
   
        
        # if error_msg:
        #     print(error_msg)
        #     return render_template('register_fail.html', msg = error_msg, dietary =dietary, travel_appetite=travel_appetite)

        # else:
        #     status = True
        #     # pw that user keyed in
        #     keyed_password = request.form.get('password')
        #     keyed_password = keyed_password.encode('utf-8')

        #     hashed = bcrypt.hashpw(keyed_password, bcrypt.gensalt(5)) 
        
        # data = request.get_json()
        # user = user_info(name, **data)

        # try:
        #     db.session.add(user)
        #     db.session.commit()
        #     db.session.commit()
        # except:
        #     return jsonify(
        #         {
        #             "code": 500,
        #             "data": {
        #                 "name": name
        #             },
        #             "message": "An error occurred creating user info."
        #         }
        # #     ), 500
        # if status:
        #     # db.session.commit()
        #     return render_template('register_success.html', name=name, username = username, password = password, status = status, dietary=dietary, travel_appetite=travel_appetite, default_address=default_address)

        
        # else:
        #     return 'Wrong password...', 400  # 400 Bad Request

# if request.method =='POST':
#         status = False
#         # these are the inputs
#         username = request.form.get('username')
#         user = user_info.query.filter_by(username=username).first()

#         # pw that user keyed in
#         keyed_password = request.form.get('password')
#         keyed_password = keyed_password.encode('utf-8')

#         # pw that is stored in db
#         password =  user.password
#         password = password.encode('utf-8')
#         hashed = bcrypt.hashpw(password, bcrypt.gensalt(5)) 

#         if bcrypt.checkpw(keyed_password, hashed):
#             print("login success")
#             status = True
#         else:
#             print("incorrect password")

#         if status:
#             return render_template('after_login.html', username = username, keyed_password = keyed_password, password = password, hashed = hashed, status = status)
#         else:
#             return 'Wrong password...', 400  # 400 Bad Request

# search user by username
# @app.route("/search/user", methods=['POST', 'GET'])
# def find_user():
#     if request.method =='POST':
#         # these are the inputs
#         name = request.form.get('name')
#         latitude = request.form.get('latitude')
#         longitude = request.form.get('longitude')
#         form = request.form
#         user = user_info.query.filter_by(name=name).first()
#         all = user_info.query.all()
        
#         # over here i updating the db lat lng 
#         user.longitude = longitude
#         user.latitude = latitude
#         # here then commit
#         db.session.commit()

#         if name and user:
#             return render_template('search_user.html', all=all, name=name, data=user, form=form, longitude=longitude, latitude=latitude)
#         else:
#             return 'Please go back and enter a valid name...', 400  # 400 Bad Request
 
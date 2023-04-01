#!/usr/bin/env python3
# import relevant dependencies
import os
import haversine as hs
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
from datetime import datetime
import uuid
import json

# INITIALISING APP
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/food_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.name == "nt":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/food_db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/food_db'

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

# DECLARING DATABASE CLASS
class food_table(db.Model):
    __tablename__ = 'food_table'

    post_id = db.Column(db.VARCHAR(64), primary_key=True)
    username = db.Column(db.VARCHAR(64), nullable=False) # username of creator
    post_name = db.Column(db.VARCHAR(64), nullable=False)
    latitude =  db.Column(db.Float(precision=6), nullable=False)
    longitude = db.Column(db.Float(precision=6), nullable=False)
    address = db.Column(db.VARCHAR(128), nullable=False)
    description = db.Column(db.VARCHAR(248))
    is_available = db.Column(db.Integer(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=False)

    def __init__(self, post_id, username, post_name, latitude, longitude, address, description, is_available, end_time):
        self.post_id = post_id
        self.username = username # username of creator
        self.post_name = post_name
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.description = description
        self.is_available = is_available
        self.end_time = end_time

    def json(self):
        post = {
            'post_id': self.post_id,
            'username': self.username, # username of creator
            'post_name': self.post_name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'description': self.description,
            'is_available' : self.is_available,
            'end_time' : self.end_time
        }
        return post

class diet_table(db.Model):
    __tablename__ = 'dietary_table'

    post_id = db.Column(db.VARCHAR(64), db.ForeignKey('food_table.post_id'), primary_key=True)
    diets_available = db.Column(db.VARCHAR(64), primary_key=True)

    def __init__(self, post_id, diets_available):
        self.post_id = post_id
        self.diets_available = diets_available
    
    def json(self):
        diet = {
            'post_id': self.post_id,
            'diets_available': self.diets_available
        }
        return diet
    
'''SHOW ALL AVAILABLE POSTS
this function shows all posts that are available
input: None, access this using the URL
output: list of post JSONs
'''
@app.route("/all", methods=['GET'])
def all():
    posts_data = food_table.query.filter_by(is_available=1).all()
    print("Getting all available posts from database...")
    if posts_data:
        output_list = []
        for post in posts_data:
            # prepare data JSON output
            data = {}
            data["post_id"] = post.post_id
            data["post_name"] = post.post_name
            data["creator"] = post.username
            data["latitude"] = post.latitude
            data["longitude"] = post.longitude
            data["address"] = post.address
            data["description"] = post.description
            data["is_available"] = post.is_available
            data["end_time"] = post.end_time

            # retrieve list of diets in post
        
            diet_list = []
            post_diets_available = diet_table.query.filter_by(post_id=post.post_id)
            for entry in post_diets_available:
                diet_list.append(entry.__dict__["diets_available"])

            data["diets_available"] = diet_list # list of diets for post
            output_list.append(data)
        
        print("Available posts retrieved!")
        return jsonify(
            {
                "code": 200,
                "data": {
                    "food": output_list
                }
            }
        )
    
    else:
        print("No available food!")
        return jsonify(
            {
                "code": 404,
                "message": "There is no available food."
            }
        ), 404

'''CREATE A POST
this function creates a post
input: JSON of the new post. it must have:
{
    "username": "actual_username",
    "post_name": "actual_postname",
    "latitude": 1.296568,
    "longitude": 103.852119,
    "address": "81 Victoria St, Singapore 188065",
    "description": "long_description",
    "end_time" : "YYYY-MM-DD HH:MI:SS",
    "diets_available": ["prawn-free", "halal", "nut-free"]
}
output: JSON of either success or failure of creation
'''
@app.route("/create_post", methods=['POST'])
def create_post():
    #if json, try adding
    if request.is_json:
        data = request.get_json()
        print("Adding post into database...")
        
        #if successful add
        if add_to_db(data) == True:
            print("Post added successfully!")
            return jsonify(
            {
                "code": 201,
                "data": {
                    "post": data
                },
                "message": "Post created successfully"
            }
        ), 201
        
    else:
        print("Error adding post into database: ")
        print(add_to_db(data))
        return add_to_db(data)
   
def add_to_db(data):
    '''
    this function adds a post into the database for create_post
    input: post json
    output: true if successful, json error description if failed
    '''   
    data["post_id"] = create_id()
    data["is_available"] = 1 # to show that post is currently available
    diet = data["diets_available"] # e.g. ["no prawns", "halal", "nuts"]
    del data["diets_available"] # to set up JSON to send into food_table, since it does not have a diets field

    try:
        # adds entry into food table
        post = food_table(**data)
        db.session.add(post)
        db.session.commit()

        # adds entries into diet table, based on diets of the post
        if diet:
            for item in diet:
                diet_row = diet_table(post_id=data["post_id"],diets_available=item)
                db.session.add(diet_row)
                db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "code":500,
                "message": "Cannot add post. System Message: " + str(e)
            }
        ), 500
    
    return True

def create_id():
    '''
    this function creates a new id for the incoming new post and checks if the id already exists in database
    input: nothing
    output: id of new post
    '''
    exist = True
    while exist:
        new_post_id = str(uuid.uuid4())
        exist = food_table.query.filter_by(post_id=new_post_id).first()
    
    return new_post_id

'''DELETE A POST
this function deletes a post given a post_id
input: none, just indicate the post_id to delete via URL
output: JSON of either success or failure of deletion
'''
@app.route("/delete/<post_id>", methods=['DELETE'])
def delete(post_id):
    print("Deleting post...")
    post = food_table.query.filter_by(post_id=post_id).first()
    #check if post exists
    if not post:
        return jsonify(
        {
            "code": 404,
            "data": {
                "post_id": post_id
            },
            "message": "Post not found."
        }
    )
    else:
        try:
            delete_diets_table(post_id)
            db.session.delete(post)
            db.session.commit()

            #if no errors, return success message
            print("Post successfully deleted!")
            print()
            return jsonify(
                {
                    "code": 201,
                    "data": post.json(),
                    "message":"Post successfully deleted."
                }
            ), 201
        
        #if post cannot be deleted, return error message
        except Exception as e:
            print("Error occured while updating the post.")
            print()
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "post_id": post_id
                    },
                    "message": "An error occurred while deleteing the post. System Message: " + str(e)
                }
            ), 500
        
def delete_diets_table(post_id):
    '''
    this function removes all diets given a post_id
    input: post_id
    output: True if successful, JSON error msg if failure
    '''
    # remove all current diets
    current_diets = diet_table.query.filter_by(post_id=post_id)
    if current_diets:
        try:
            for entry in current_diets:
                db.session.delete(entry)
                db.session.commit()
            return True

        except Exception as e:
            return jsonify(
                {
                    "code":500,
                    "message": "System Error Message: " + str(e)
                }
            ), 500
        
'''EDIT A POST
this function edits a post given a post_id
input: updated full JSON of new post, it must have:
{
    "username": "actual_username",
    "post_name": "actual_postname",
    "latitude": 1.296568,
    "longitude": 103.852119,
    "address": "81 Victoria St, Singapore 188065",
    "description": "long_description",
    "end_time" : "YYYY-MM-DD HH:MI:SS",
    "diets_available": ["prawn-free", "halal", "nut-free"],
    "is_available": 0
}
output: JSON message of either success or failure of edit
'''
@app.route("/edit/<post_id>", methods=['PUT'])
def edit(post_id):
    print("Editing post...")
    post = food_table.query.filter_by(post_id=post_id).first()

    # if post does not exist
    if not post:
        # notify that post does not exist
        print("Post does not exist!")
        print()

        return jsonify(
            {
                "code": 404,
                "data": {
                    "post_id": post_id
                },
                "message": "Post does not exist."
            }
        ), 404

    else:
        #attempt to edit
        try:
            data = request.get_json()

            #update fields
            post.username = data['username']
            post.post_name = data['post_name']
            post.latitude = data['latitude'] 
            post.longitude = data['longitude'] 
            post.address = data['address']
            post.description = data['description']  
            post.is_available = data['is_available'] 
            db.session.commit()

            edit_diets_table(post_id,data['diets_available'])
           
            #if no errors, return success message
            print("Post edited successfully!")
            return jsonify(
                {
                    "code": 200,
                    "message": "Post edited successfully."
                }
            ), 200
        
        #if post cannot be edited, return error message
        except Exception as e:
            print("Error occured while updating the post.")
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "post_id": post_id
                    },
                    "message": "An error occurred while updating the post. System Message: " + str(e)
                }
            ), 500
            
def edit_diets_table(post_id, diet_list):
    '''
    this function removes all current diets and re-adds diets
    input: post_id that is being created, list of diets
    output: True if successful, JSON error msg if failure
    '''
    # remove all current diets
    current_diets = diet_table.query.filter_by(post_id=post_id)
    for entry in current_diets:
        db.session.delete(entry)
        db.session.commit()

    try:
        for item in diet_list:
            # if current table has a diet that is now being removed
            diet_row = diet_table(post_id=post_id,diets_available=item)
            db.session.add(diet_row)
            db.session.commit()
        
        return True

    except Exception as e:
        return jsonify(
            {
                "code":500,
                "message": "System Error Message: " + str(e)
            }
        ), 500
    
'''NEARBY FOOD FOR USER
Function: search for food posts which are within a specified user's travel appetite and user's dietary requirements
Input: user JSON object, it must include:
{
    "latitude": 1.296273,
    "longitude": 103.850158,
    "dietary_type": ["halal","no prawns"],
    "travel_appetite": 2
}
Output: array of food post JSON objects that fulfill the criteria
'''
@app.route("/nearby_food_user", methods=['GET'])
def nearby_food_user():
    # check input format and data is JSON
    if not request.is_json:
        data = request.get_data()
        print("Received an invalid user!")
        print(data)
        print()
        return jsonify(
            {
                "code": 403,
                "data": data,
                "message": "Request is not in JSON. System message: " + str(e)
            }
        ), 403

    else:
        try:
            print("Finding nearby food...")
            user = request.get_json()
            all_posts = food_table.query.all()
            filtered_posts = []

            # filter for posts within specified user's travel appetite
            for post in all_posts:
                user_latitude = user['latitude']
                user_longitude = user['longitude']

                # prepare data JSON output
                data = {}
                data["post_id"] = post.post_id
                data["post_name"] = post.post_name
                data["creator"] = post.username
                data["latitude"] = post.latitude
                data["longitude"] = post.longitude
                data["address"] = post.address
                data["description"] = post.description
                data["is_available"] = post.is_available
                data["end_time"] = post.end_time

                # retrieve list of diets in post
                diet_list = []
                post_diets_available = diet_table.query.filter_by(post_id=post.post_id)
                for entry in post_diets_available:
                    diet_list.append(entry.__dict__["diets_available"])

                data["diets_available"] = diet_list # list of diets for post

                # get distance from user to post
                distance = hs.haversine((post.latitude,post.longitude),(user_latitude, user_longitude))              
                if check_if_valid(distance,diet_list,user,post):
                    filtered_posts.append(data)
            print("Found nearby food!")
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "user": filtered_posts
                    }
                }
            )
    
        except Exception as e:
            return jsonify(
                {
                    "code": 404,
                    "message": "Error occurred. System message: " + str(e)
                }
            ), 404
        
def check_if_valid(distance,diet_list,user,post):
    '''
    this function checks if a post is a valid post
    input: distance of post to user, diets_availability of post, user JSON
    output: True if valid, False otherwise
    '''
    if user["travel_appetite"] > distance and post.__dict__["is_available"] == 1:
        for diet in user["dietary_type"]:
            if diet not in diet_list:
                return False

        return True
    else:
        return False

'''NEARBY FOOD GUEST
Function: search for food posts which are within a specified user's travel appetite and user's dietary requirements
Input: user JSON object, it must include:
{
    "latitude": 1.296273,
    "longitude": 103.850158
}
Output: array of food post JSON objects that fulfill the criteria

'''
@app.route("/nearby_food_guest", methods=['GET'])
# search for users that are within the distance
def nearby_food_guest():
    # check input format and data is JSON
    if request.is_json:
        try:
            print("Finding nearby food...")
            user = request.get_json()
            all_posts = food_table.query.all()
            filtered_posts = []

            # filter for posts within specified user's travel appetite
            for post in all_posts:
                user_latitude = user['latitude']
                user_longitude = user['longitude']

                # prepare data JSON output
                data = {}
                data["post_id"] = post.post_id
                data["post_name"] = post.post_name
                data["creator"] = post.username
                data["latitude"] = post.latitude
                data["longitude"] = post.longitude
                data["address"] = post.address
                data["description"] = post.description
                data["is_available"] = post.is_available
                data["end_time"] = post.end_time

                diet_list = []
                post_diets_available = diet_table.query.filter_by(post_id=post.post_id)
                for entry in post_diets_available:
                    diet_list.append(entry.__dict__["diets_available"])

                data["diets_available"] = diet_list # list of diets for post

                # preset the TA to 2km here
                user_travel_appetite = 2
                distance = hs.haversine((post.latitude,post.longitude),(user_latitude, user_longitude))
                if distance <= user_travel_appetite:
                    filtered_posts.append(data)
                    # list of food post objects where the post is within the user's travel appetite

            print("Found nearby food!")
            
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "posts": filtered_posts
                    }
                }
            )
    
        except Exception as e:
            return jsonify(
                {
                    "code": 404,
                    "message": "Error occurred. System message: " + str(e)
                }
            ), 404

'''FIND POSTS BASED ON USERNAME
This function returns a list of posts based on username
Input: None, parse username through URL
Output: A list of post jsons
'''
@app.route("/filter_user/<string:username>")
def filter_user(username):
    posts_data = food_table.query.filter_by(username=username).all()
    output_list = []
    if posts_data:
        for post in posts_data:
            # prepare data JSON output
            data = {}
            data["post_id"] = post.post_id
            data["post_name"] = post.post_name
            data["creator"] = post.username
            data["latitude"] = post.latitude
            data["longitude"] = post.longitude
            data["address"] = post.address
            data["description"] = post.description
            data["is_available"] = post.is_available
            data["end_time"] = post.end_time

            # retrieve list of diets in post
        
            diet_list = []
            post_diets_available = diet_table.query.filter_by(post_id=post.post_id)
            for entry in post_diets_available:
                diet_list.append(entry.__dict__["diets_available"])

            data["diets_available"] = diet_list # list of diets for post
            if data["creator"] == username:
                output_list.append(data)
            
        return output_list
    else:
        return {

        }
if __name__ == '__main__':
    app.run(port=1112, debug=True)

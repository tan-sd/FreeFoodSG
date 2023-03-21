#!/usr/bin/env python3
# import relevant dependencies
import os
import haversine as hs
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


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
class diet_table(db.Model):
    __tablename__ = 'dietary_table'

    post_id = db.Column(db.Integer, ForeignKey('food_table.post_id', ondelete="CASCADE"), primary_key=True)
    dietary_type = db.Column(db.VARCHAR(64), primary_key=True)

    def __init__(self, post_id, dietary_type):
        self.post_id = post_id
        self.dietary_type = dietary_type
    
    def json(self):
        diet = {
            'post_id': self.post_id,
            'dietary_type' : self.dietary_type
        }
        return diet

class food_table(db.Model):
    __tablename__ = 'food_table'

    post_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(64), nullable=False) # username of creator
    post_name = db.Column(db.VARCHAR(64), nullable=False)
    latitude =  db.Column(db.Float(precision=6), nullable=False)
    longitude = db.Column(db.Float(precision=6), nullable=False)
    address = db.Column(db.VARCHAR(128), nullable=False)
    description = db.Column(db.VARCHAR(248))
    is_available = db.Column(db.Integer(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=False)
    photo_name = db.Column(db.VARCHAR(64))
    photo_path = db.Column(db.VARCHAR(128))
    diets = relationship("diet_table", backref="food_table")

    def __init__(self, post_id, username, post_name, latitude, longitude, address, description, is_available, end_time, photo_name, photo_path):
        self.post_id = post_id
        self.username = username # username of creator
        self.post_name = post_name
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.description = description
        self.is_available = is_available
        self.end_time = end_time
        self.photo_name = photo_name
        self.photo_path = photo_path

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
            'end_time' : self.end_time,
            'photo_name' : self.photo_name,
            'photo_path' : self.photo_path
        }
        return post

# SHOW ALL POSTS

@app.route("/")
def main_page():
    return 'this is the main page'

@app.route("/all")
def all():
    food_list = food_table.query.all()
    if len(food_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "food": [food.json() for food in food_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There is no food."
        }
    ), 404

# RETRIEVE SPECIFIC POST
@app.route("/search/<int:post_id>")
def find_post(post_id):
    post = food_table.query.filter_by(post_id=post_id).first()

    #if post exists, return post json
    if post:
        return jsonify(
            {
                "code": 200,
                "data": post.json()
            }
        )
    
    #else, return error message
    return jsonify(
        {
            "code": 404,
            "message": "Post not found."
        }
    ), 404

# CREATE A POST
@app.route("/create>", methods=['POST'])
def create_post():

    #check if post is already in the db
    data = request.get_json()
    post = food_table(**data, is_available=1)

    #attempt to add post into db
    try:
        db.session.add(post)
        db.session.commit()

    #if post cannot be made, return error message
    except:
        return jsonify(
            {
                "code":500,
                "message": "An error occurred when creating a post. Please check if all fields meet the constraints of the database."
            }
        ), 500
    
    #if no errors, return success message
    return jsonify(
        {
            "code": 201,
            "data": post.json(),
            "message": "Post created successfully."
        }
    ), 201

# DELETE A POST
@app.route("/delete/<int:post_id>", methods=['DELETE'])
def delete(post_id):
    post = food_db.query.filter_by(post_id=post_id).first()

    #check if post exists
    if post:

        #attempt to delete post from db
        try:
            db.session.delete(post)
            db.session.commit()

        #if post cannot be deleted, return error message
        except:
             return jsonify(
            {
                "code": 500,
                "data": {
                    "post_id": post_id
                },
                "message": "An error occurred when deleting the post. Please check if the post still exists."
            }
        ), 500

        #if no errors, return success message
        return jsonify(
            {
                "code": 201,
                "data": post.json(),
                "message":"Post successfully deleted."
            }
        ), 201
        
    #else, notify that the post doesn't exist
    return jsonify(
        {
            "code": 404,
            "data": {
                "post_id": post_id
            },
            "message": "Post not found."
        }
    )

# EDIT A POST (SEND A JSON WITH UPDATED PARTICULARS)
@app.route("/edit/<int:post_id>", methods=['PUT'])
def edit(post_id):
    
    post = food_db.query.filter_by(post_id=post_id).first()

    #check if post exists
    if post:

        #attempt to edit
        try:
            data = request.get_json()

            #update fields
            post.post_name = data['post_name']
            post.latitude = data['latitude'] 
            post.longitude = data['longitude'] 
            post.description = data['description']  
            post.allergens = data['allergens'] 
            post.is_available = data['is_available'] 

            #commit changes
            db.session.commit()

            #if no errors, return success message
            return jsonify(
                {
                    "code": 200,
                    "data": post.json(),
                    "message": "Post edited successfully. See above for updated post details."
                }
            ), 200
        
        #if post cannot be edited, return error message
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "post_id": post_id
                    },
                    "message": "An error occurred while updating the post. " + str(e)
                }
            ), 500
            
    #else, notify that post does not exist
    return jsonify(
        {
            "code": 404,
            "data": {
                "post_id": post_id
            },
            "message": "Post not found."
        }
    ), 404

# TO TEST IF FOREIGN KEY FUNCTION WORKS
@app.route("/test")
def test():
    post = food_table.query.filter_by(post_id=1).first()
    if post:
        # check diets of the post by accessing .diets, which accesses dietary_table
        diet_list = post.diets
        return jsonify({
            "code":200,
            "diets": [restriction.json()["dietary_type"] for restriction in post.diets]
        }) 
    return jsonify(
        {
            "code": 404,
            "message" : "Post does not exist"
        }
    ), 404

'''
Details for wrapper function below

Function: search for food posts which are within a specified user's travel appetite and user's dietary requirements
Input: user JSON object
Output: array of food post JSON objects that fulfill the criteria
'''
# NEED TO FILTER ACCORDING TO ALLERGY TOO

@app.route("/filter_post", methods=['GET'])

# search for users that are within the distance
def filter_post():
    # check input format and data is JSON
    if request.is_json:
        try:
            # get query info
            query = request.get_json()
            print("\nReceived a query in JSON:", query)

            # do the actual checking
            # return list of food post objects from food_dB
            all_food_info = food_table.query.all()
            filtered_food = []
            if len(all_food_info):
                # filter for posts within specified user's travel appetite
                for food in all_food_info:
                    
                    post_id = food.post_id
                    food_latitude = food.latitude
                    food_longitude = food.longitude
                    user_latitude = query['latitude']
                    user_longitude = query['longitude']
                    user_travel_appetite = query['travel_appetite']
                    distance = hs.haversine((food_latitude,food_longitude),(user_latitude, user_longitude))

                    # check dietary_list of the post by accessing .diets, which accesses dietary_table
                    user_dietary_type = query['dietary_type']
                    food_dietary_list = food.diets[0].query.filter_by(post_id=post_id)

                    diet_list = []
                    for diets in food_dietary_list:
                        diet_list.append(diets.dietary_type)

                    if distance <= user_travel_appetite and user_dietary_type in diet_list:
                        filtered_food.append(food)
                
                    

                return jsonify(
                    {
                        "code":200,
                        "data":{
                            "filtered_food": [x.json() for x in filtered_food]
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
        except Exception as e:
            return jsonify(
                {
                    "code": 404,
                    "message": "Error occurred. System message: " + str(e)
                }
            ), 404

# for guest users
@app.route("/nearby_food", methods=['GET'])
# search for users that are within the distance
def guest_display():
    # check input format and data is JSON
    if request.is_json:
        try:
            # get query info
            query = request.get_json()
            print("\nReceived a query in JSON:", query)

            # do the actual checking
            # return list of food post objects from food_dB
            all_food_info = food_db.query.all()
            filtered_food = []
            if len(all_food_info):
                # filter for posts within specified user's travel appetite
                for food in all_food_info:
                    food_latitude = food.latitude
                    food_longitude = food.longitude
                    user_latitude = query['latitude']
                    user_longitude = query['longitude']

                    # preset the TA to 2km here
                    user_travel_appetite = 2
                    distance = hs.haversine((food_latitude,food_longitude),(user_latitude, user_longitude))

                    if distance <= user_travel_appetite:
                        filtered_food.append(food)
                # return list of food post objects where the post is within the user's travel appetite
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "user": [info.json() for info in filtered_food]
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
        except:
            pass


if __name__ == '__main__':
    app.run(port=1112, debug=True)

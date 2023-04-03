#!/usr/bin/env python3
# import relevant dependencies
import os
import haversine as hs
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

# INITIALISING APP
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.name == "nt":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/forum_db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/forum_db'

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

# DECLARING DATABASE CLASS
class forum_db(db.Model):
    __tablename__ = 'forum_table'
    forum_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(64), nullable=False)
    title =  db.Column(db.VARCHAR(64), nullable=False)
    description = db.Column(db.VARCHAR(1000))
    is_available = db.Column(db.Integer(), nullable=False)
    datetime = db.Column(db.DateTime(19), nullable=False)
    

    def __init__(self, forum_id, username, title, description, is_available, datetime):
        self.forum_id = forum_id
        self.username = username
        self.title = title
        self.description = description
        self.is_available = is_available
        self.datetime = datetime


    def json(self):
        forum = {
            'forum_id': self.forum_id,
            'username': self.username,
            'title': self.title,
            'description': self.description,
            'is_available' : self.is_available,
            'datetime': self.datetime
        }
        return forum
    
class comments_table(db.Model):
    tablename = 'comments_table'
    forum_id = db.Column(db.Integer, db.ForeignKey('forum_table.forum_id'), primary_key=True)
    commentor_username = db.Column(db.VARCHAR(64), nullable=False, primary_key=True)
    comment =  db.Column(db.VARCHAR(1000), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, primary_key=True)
    
    def init(self, forum_id, commentor_username, comment, datetime):
        self.forum_id = forum_id
        self.commentor_username = commentor_username
        self.comment = comment
        self.datetime = datetime


    def json(self):
        forum = {
            'forum_id': self.forum_id,
            'commentor_username': self.commentor_username,
            'comment': self.comment,
            'datetime': self.datetime
        }
        return forum

''' SHOW ALL FORUM POSTS WITH COMMENTS
this function show all posts
input: 
nothing

output: 

{
    "code": 200,
    "data": {
        "forum": [
            {
                "comments": [
                    {
                        "comment": "comment2",
                        "commentor_username": "SJB123",
                        "datetime": "Wed, 01 Jan 2020 15:10:10 GMT",
                        "forum_id": 1
                    },
                    {
                        "comment": "comment1",
                        "commentor_username": "SJB123",
                        "datetime": "Mon, 03 Apr 2023 15:51:48 GMT",
                        "forum_id": 1
                    }
                ],
                "datetime": "Fri, 01 Jan 2021 15:10:10 GMT",
                "description": "description1",
                "forum_id": 1,
                "is_available": 1,
                "title": "title1",
                "username": "SJB123"
            },
            {
                "comments": [
                    {
                        "comment": "comment1",
                        "commentor_username": "DA123",
                        "datetime": "Mon, 03 Apr 2023 15:51:48 GMT",
                        "forum_id": 2
                    }
                ],
                "datetime": "Fri, 01 Jan 2021 15:10:10 GMT",
                "description": "description2",
                "forum_id": 2,
                "is_available": 1,
                "title": "title2",
                "username": "SJB123"
            },
            {
                "comments": [],
                "datetime": "Sat, 01 Jan 2022 15:10:10 GMT",
                "description": "description3",
                "forum_id": 3,
                "is_available": 1,
                "title": "title3",
                "username": "SJB123"
            }
        ]
    }
}

'''

# SHOW ALL FORUM POSTS (only available ones)
@app.route("/all", methods=['GET'])
def all():

    forum_list = forum_db.query.filter_by(is_available=1).all()
    comments_list = comments_table.query.all()
    output = []
    comments = [comment.json() for comment in comments_list]

    comments_obj = {}
    for comment in comments:
        id = comment['forum_id']
        if comments_obj.get(id) == None:
            comments_obj[id] = [comment]
        else:
            comments_obj[id].append(comment)

    for e_post in forum_list:
        e_post = e_post.json()
        e_id = e_post['forum_id']

        if e_id in comments_obj:
            e_post['comments'] = comments_obj[e_id]
        else:
            e_post['comments'] = []
        
        output.append(e_post)

    if len(forum_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "forum": output
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no forum posts."
        }
    ), 404



'''DISPLAY SPECFIC FORUM POST DETAILS
this function finds a post details
input: it must have:

nothing, just put forum_id in the url

output: 

{
    "code": 200,
    "data": {
        "datetime": "Fri, 01 Jan 2021 15:10:10 GMT",
        "description": "description1",
        "forum_id": 1,
        "title": "title1",
        "username": "SJB123",
        "is_available": 1,
    }
}

'''

# RETRIEVE SPECIFIC FORUM POST BY USERNAME
@app.route("/search/<string:username>", methods=['GET'])
def search(username):
    forum = forum_db.query.filter_by(username=username).all()
    result = []
    for e_post in forum:
        e_post = e_post.json()
        result.append(e_post["forum_id"])
    #if forum exists, return forum json
    if forum:
        return jsonify(
            {
                "code": 200,
                "data": result
            }
        )
    
    #else, return error message
    return jsonify(
        {
            "code": 404,
            "message": "Post not found."
        }
    ), 404

# RETRIEVE SPECIFIC FORUM POST BY FORUM_ID
@app.route("/search_id/<int:forum_id>", methods=['GET'])
def search_id(forum_id):
    forum = forum_db.query.filter_by(forum_id=forum_id).first()

    #if forum exists, return forum json
    if forum:
        return jsonify(
            {
                "code": 200,
                "data": forum.json()
            }
        )
    
    #else, return error message
    return jsonify(
        {
            "code": 404,
            "message": "Post not found."
        }
    ), 404

'''CREATE FORUM POST
this function creates post
input: it must have:

{          
    "username": "tommy",
    "title": "free french fries",
    "description": "I had a party just now! You are welcome to join.",
    "datetime": "2021-01-01 15:10:10",
    "is_available": 1,
}

output: 

{
    "code": 201,
    "data": {
        "datetime": "Fri, 01 Jan 2021 15:10:10 GMT",
        "description": "I had a party just now! You are welcome to join.",
        "forum_id": 4,
        "title": "free french fries",
        "username": "tommy",
        "is_available": 1,
    },
    "message": "Post created successfully."
}

'''

# CREATE A FORUM POST
@app.route("/create", methods=['POST'])
def create():
    
    data = request.get_json()
    forum_id = forum_db.query.order_by(forum_db.forum_id.desc()).first().forum_id
    data["forum_id"] = forum_id + 1
    
    forum = forum_db(**data)

    #attempt to add post into db
    try:
        db.session.add(forum)
        db.session.commit()

    #if post cannot be made, return error message
    except Exception as e:
        return jsonify(
            {
                "code":500,
                "data":{
                    "forum_id":forum_id
                },
                "message": "An error occurred when creating a post. System Error Message: " + str(e)
            }
        ), 500
    
    #if no errors, return success message
    return jsonify(
        {
            "code": 201,
            "data": forum.json(),
            "message": "Post created successfully."
        }
    ), 201



'''EDIT FORUM POST
this function puts edit post to unavailable
input: it must have:

{
    "datetime": "2021-01-01 15:10:10",
    "description": "description1",
    "forum_id": 1,
    "is_available": 0,
  
        
}

output: 

{
    "code": 200,
    "data": {
        "datetime": "Fri, 01 Jan 2021 15:10:10 GMT",
        "description": "description1",
        "forum_id": 1,
        "is_available": 0,
        "title": "title1",
        "username": "SJB123"
    },
    "message": "Post edited successfully. See above for updated forum post details."
}
'''

# EDIT A POST (SEND A JSON WITH UPDATED PARTICULARS)
@app.route("/edit/<int:forum_id>", methods=['PUT'])
def edit(forum_id):
    
    forum = forum_db.query.filter_by(forum_id=forum_id).all()

    #check if post exists
    if forum:

        #attempt to edit
        try:

            #update fields
            forum.is_available = 0

            #commit changes
            db.session.commit()
            print("Post edited successfully!")

            #if no errors, return success message
            return jsonify(
                {
                    "code": 200,
                    "data": forum.json(),
                    "message": "Post edited successfully. See above for updated forum post details."
                }
            ), 200
        
        #if post cannot be edited, return error message
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "forum_id": forum_id
                    },
                    "message": "An error occurred while updating the post. " + str(e)
                }
            ), 500
            
    #else, notify that post does not exist
    return jsonify(
        {
            "code": 404,
            "data": {
                "forum_id": forum_id
            },
            "message": "Post not found."
        }
    ), 404


# FOR COMMENTS ROUTES

'''GET ALL COMMENTS FROM ALL THE POSTS
this function returns all comments
input: it must have:

nothing

output: 

{
    "code": 200,
    "data": {
        "comments": [
            {
                "comment": "comment2",
                "commentor_username": "SJB123",
                "datetime": "Wed, 01 Jan 2020 15:10:10 GMT",
                "forum_id": 1
            },
            {
                "comment": "comment1",
                "commentor_username": "SJB123",
                "datetime": "Sun, 02 Apr 2023 08:07:55 GMT",
                "forum_id": 1
            },
            {
                "comment": "comment1",
                "commentor_username": "DA123",
                "datetime": "Sun, 02 Apr 2023 08:07:55 GMT",
                "forum_id": 2
            }
        ]
    }
}

'''

# this is to get all the comments from all the posts
@app.route("/comment", methods=['GET'])
def all_comments():

   comments_list = comments_table.query.all()
   if len(comments_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "comments": [comment.json() for comment in comments_list]
                }
            }
        )
   return jsonify(
        {
            "code": 404,
            "message": "There are no comments."
        }
    ), 404


'''GET ALL COMMENTS FROM 1 specific post
this function returns all comments for tat post
input: it must have:

nothing, just put forum_id in url

output: 

{
    "code": 200,
    "data": {
        "user": [
            {
                "comment": "comment2",
                "commentor_username": "SJB123",
                "datetime": "Wed, 01 Jan 2020 15:10:10 GMT",
                "forum_id": 1
            },
            {
                "comment": "comment1",
                "commentor_username": "SJB123",
                "datetime": "Sun, 02 Apr 2023 08:07:55 GMT",
                "forum_id": 1
            }
        ]
    }
}

'''
# this is to get all the comments from 1 post
@app.route("/comment/<int:forum_id>", methods=['GET'])
def show_comments(forum_id):

   comments = comments_table.query.filter_by(forum_id=forum_id).all()
   if len(comments):
       return jsonify(
            {
                "code": 200,
                "data": {
                    "user": [info.json() for info in comments]
                }
            }
        )
    
   return jsonify(
        {
            "code": 404,
            "message": "There are no comments."
        }
    ), 404




'''create comment on a specific post
this function create comments
input: it must have:

 {
    "comment": "new comment",
    "commentor_username": "SJB123",
    "datetime": "2021-01-01 15:10:10",
    "forum_id": 1
}

output: 

{
    "code": 201,
    "data": {
        "comment": "new comment",
        "commentor_username": "SJB123",
        "datetime": "Fri, 01 Jan 2021 15:10:10 GMT",
        "forum_id": 1
    },
    "message": "Comment created successfully."
}

'''

# this is to add comments to the specific post
@app.route("/create_comment", methods=['POST'])
def create_comment():
    data = request.get_json()
    forum_id = data['forum_id']

    #check if forum post ID is already in the db
    if(forum_db.query.filter_by(forum_id=forum_id).first()):
        forum = comments_table(**data)

        #attempt to add post into comment table
        try:
            db.session.add(forum)
            db.session.commit()

        #if post cannot be made, return error message
        except Exception as e:
            return jsonify(
                {
                    "code":500,
                    "data":{
                        "forum_id":forum_id
                    },
                    "message": "An error occurred when creating comment. System Error Message: " + str(e)
                }
            ), 500
        
        #if no errors, return success message
        return jsonify(
            {
                "code": 201,
                "data": forum.json(),
                "message": "Comment created successfully."
            }
        ), 201
        
    else:
        # forum post do not exist so ERROR 
        #else, carry on making the post
        return jsonify(
            {
                "code": 404,
                "data": {
                    "forum_id": forum_id
                },
                "message": "The forum post doesn't exist"
            }
        ), 404

if __name__ == '__main__':
    app.run(port=1115, debug=True)
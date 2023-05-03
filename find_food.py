from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from os import environ
from invokes import invoke_http
from invoke_activity import activity_log
app = Flask(__name__)
CORS(app)

'''
this complex service has two main functions
1) get all available nearby food that fits dietary restrictions for USER
2) get all available nearby food for GUEST (regardless of diet, travel appetite set to 2)
'''

verify_user_URL = 'http://localhost:1111/login'
register_user_URL = 'http://127.0.0.1:1111/user'
user_URL = 'http://localhost:1111/users'
nearby_food_user_URL = environ.get("user_food_URL") or 'http://localhost:1112/nearby_food_user'
nearby_food_guest_URL = environ.get("guest_food_URL") or 'http://localhost:1112/nearby_food_guest'

'''USER LOGIN
Function: verify user login
Input: JSON object -> {
    "username" : string,
    "password" : string
}
Output: user details as json 
{
    'code': 201, 
    'msg': 'Login Successfully', 
    'user': {'address': 'Victoria Street, Singapore Management University Singapore',
    'dietary_type': ["halal","prawn-free"], 
    'email': 'shengdatan@gmail.com',
    'first_name': 'Sheng Da', 
    'last_name': 'Tan', 
    'latitude': 1.296273,
    'longitude': 103.850158,
    'number': '92476862', 
    'travel_appetite': 1, 
    'user_id': 9, 
    'username': 'DA123'
}
'''
@app.route("/login", methods=['POST'])
def user_login():
    # check if JSON
    if not request.is_json:
        activity_log("login not json error")
        return jsonify({
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 400

    else:
        try:
            user_login_details = request.get_json()
            print("\nReceived username and password in JSON:", user_login_details)
            result = verification(user_login_details)
            print(jsonify(result))
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)
            activity_log("user login error")

            return jsonify({
                "code": 500,
                "message": "find_food.py internal error: " + ex_str
            }), 500

def verification(user_details):
    print('\n-----Invoking user_info microservice-----')
    print(user_details)

    url = verify_user_URL
    verification_result = invoke_http(url, method='GET', json=user_details)
    activity_log("user")
    
    print('verification_result:', verification_result)

    code = verification_result["code"]

    if code not in range(200, 300):
        activity_log("user_info error")
        return {
            "code": 500,
            "data": {"verification_result": verification_result},
            "message": "Login error."
        }
    return {
        "code": 201,
        "data": {
            "verification_result": verification_result,
        }
    }

'''USER REGISTER
Function: register the user and add user info to db
Input: JSON object -> {
    "username" : “greenapple”,
    "password" :  “password”
}
Output: user details as json 
{
    code: 201,
    data: {
    
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "number": number,
            "email": email,
            "password": password,
            "address": address,
            "latitude": latitude float,
            "longitude": longitude float,
            "dietary_type": ["halal"],
            "travel_appetite": 2
    },
    messsage: 'User created successfully'
}
'''
@app.route("/user", methods=['POST'])
def user_register():

    print('in register function')
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:

            user_login_details = request.get_json()
            print("\nReceived username and password in JSON:", user_login_details)

            # do the actual work
            result = register(user_login_details)

            # CHECK OUTPUT
            print(jsonify(result), result["code"])
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            activity_log("user_info error")
            return jsonify({
                "code": 500,
                "message": "find_food.py internal error: " + ex_str
            }), 500

    activity_log("register is not json error")
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def register(user_details):

    print('\n-----Invoking user_info microservice-----')
    print(user_details)
    # user_details['username']

    url = register_user_URL + '/' + user_details['username']
    print(url)
    creation_result = invoke_http(url, method='POST', json=user_details)
    activity_log("user") #to put in activity log

    
    print('creation_result:', creation_result)

    code = creation_result["code"]

    if code not in range(200, 300):
        activity_log("user_info error")
        return {
            "code": 500,
            "data": {"creation_result": creation_result},
            "message": "User creation failure sent for error handling."
        }
    return {
        "code": 201,
        "data": {
            "Creation_result": creation_result,
        }
    }

'''GET ALL NEARBY FOOD NEAR USER
    Function: get all available food near the user
    Input: JSON object -> {
        "latitude": 1.296273,
        "longitude": 103.850158,
        "dietary_type": ['halal','prawn-free'],
        "travel_appetite": 1
    }
    Output: list of all json food objects
    {
            "code": 201,
            "data": {
                "food_result": {
                
                    {
                            "code":200,
                            "data":{
                                "filtered_food": [x for x in filtered_food]
                            }
                    }
                
                }
    }
    '''
@app.route("/available_food", methods=['POST'])
def get_available_food():
    
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            location = request.get_json()
            print("\nReceived lat and long in JSON:", location)

            # do the actual work
            result = filtered_food(location)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            activity_log("food_info error")
            return jsonify({
                "code": 500,
                "message": "find_food.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    activity_log("avail food is not json error")
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# input: location json obj to food url
# output: list of all nearby food. this is a json with a list
def filtered_food(location):
    print('\n-----Invoking food_info microservice-----')
    food_result = invoke_http(nearby_food_user_URL, method='POST', json=location)
    activity_log("food_info") #to put in activity log
    code = food_result["code"]
    if code not in range(200, 300):
        activity_log("food_info error") #to put in activity log
        print("Food status ({:d}) sent to the error microservice:".format(
            code), food_result)
        return {
            "code": 500,
            "data": {"food_result": food_result},
            "message": "Food retrieval failure."
        }

    return {
        "code": 201,
        "data": {
            "food_result": food_result
        }
    }


# 2nd route for scenario 1
# input: lat long of user (from wifi)
# output: json obj of all nearby food in a list

'''GET ALL AVAILABLE FOOD NEAR GUEST
Function: get all available food near the user [guest user]
Input: JSON object -> {
    "latitude" : float,
    "longitude" : float
}
Output: 
return jsonify(result), result["code"]
list of all json food objects
{
    "code": 201,
    "data": {
        "food_result": 
                {
                    "code": 200,
                    "data": {
                        "user": [<post information>]
                    }
                }
}
'''

# if there is no user credentials (for guest)
@app.route("/guest/available_food", methods=['POST'])
def get_available_food2():
    if request.is_json:
        try:
            guest_details = request.get_json()
            print("\nReceived latitude and longitude in JSON:", guest_details)

            # do the actual work
            result = show_available_food(guest_details)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            activity_log("user_info error")
            return jsonify({
                "code": 500,
                "message": "find_food.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    activity_log("guest user get food is not json")
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


# show available food for guest users
def show_available_food(location):

    print('\n-----Invoking food microservice-----')
    food_result = invoke_http(nearby_food_guest_URL, method='POST', json=location)
    activity_log("food_info") #to put in activity log

    # Check the food result; if a failure, send it to the error microservice.
    code = food_result["code"]
    if code not in range(200, 300):
        activity_log("food_info_error")
        return {
            "code": 500,
            "data": {"food_result": food_result},
            "message": "Retrieve food failure sent for error handling."
        }
    
    return {
        "code": 201,
        "data": {
            "food_result": food_result
        }
    }

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5101, debug=True)
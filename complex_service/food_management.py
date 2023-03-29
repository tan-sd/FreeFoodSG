from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# to login user 
verify_user_URL = 'http://localhost:1111/login'


# SCENARIO 1: GET FOOD
# related to user_info.py
user_URL = 'http://localhost:1111/users'

# for current users
food_URL = 'http://localhost:1112/filter_post'

# for guest users
nearby_food_URL = 'http://localhost:1112/nearby_food'



# SCENARIO 3: CREATE POST ON FORUM and ADD COMMENTS

forum_URL = 'http://localhost:1113/all'
create_forum_URL = 'http://localhost:1113'



# do error microservice
error_URL = ''

# scenario 1: user retrieves a list of nearby buffets

# just verification
@app.route("/login", methods=['GET', 'POST'])
def user_login():

    # input is {username : lala,
    #           password: 123}    
    # }

    # Simple check of input format and data of the request are JSON
    print('in login function')
    if request.is_json:
        try:
            # may need to sep login and displaying??
            user_login_details = request.get_json()
            print("\nReceived username and password in JSON:", user_login_details)

            # do the actual work
            result = verfication(user_login_details)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "food_management.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def verfication(user_details):

    print('\n-----Invoking user_info microservice-----')
    print(user_details)

    url = verify_user_URL
    verification_result = invoke_http(url, method='POST', json=user_details)
    
    print('verification_result:', verification_result)

    code = verification_result["code"]

    # DO ERROR MS!
    if code not in range(200, 300):

    #     # Inform the error microservice
    #     print('\n\n-----Invoking error microservice as order fails-----')
    #     invoke_http(error_URL, method="POST", json=verification_result)
    #     # - reply from the invocation is not used; 
    #     # continue even if this invocation fails
    #     print("Order status ({:d}) sent to the error microservice:".format(
    #         code), verification_result)

    #     # 7. Return error
        return {
            "code": 500,
            "data": {"order_result": verification_result},
            "message": "Order creation failure sent for error handling."
        }
    return {
        "code": 201,
        "data": {
            "verification_result": verification_result,
        }
    }
# END OF VERIFICATION FUNCTION AND M/S



# this input will be {'latitude' :123, 'longitude':456}
@app.route("/available_food", methods=['GET'])
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

            return jsonify({
                "code": 500,
                "message": "food_management.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


# input: location json obj to food url
# output: list of all nearby food. this is a json with a list
def filtered_food(location):

    # we already have the location, so we check w food m/s
    print('\n-----Invoking food_info microservice-----')
    food_result = invoke_http(food_URL, method='POST', json=location)
    print('food_result:', food_result)

    # itll filter according to user TA and allergy

    code = food_result["code"]
    if code not in range(200, 300):

        # Inform the error microservice
        print('\n\n-----Invoking error microservice as order fails-----')
        invoke_http(error_URL, method="POST", json=food_result)
        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("Food status ({:d}) sent to the error microservice:".format(
            code), food_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"food_result": food_result},
            "message": "Food Retrieval failure sent for error handling."
        }

    # 7. Return food result -> all the food to be displayed
    return {
        "code": 201,
        "data": {
            "food_result": food_result
        }
    }


# 2nd route for scenario 1
# input: lat long of user (from wifi)
# output: json obj of all nearby food in a list

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

            return jsonify({
                "code": 500,
                "message": "food_management.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


# show available food for guest users
def show_available_food(location):

    print('\n-----Invoking food microservice-----')
    food_result = invoke_http(food_URL, method='GET', json=location)
    print('food_result:', food_result)

    # Check the food result; if a failure, send it to the error microservice.
    code = food_result["code"]
    if code not in range(200, 300):

    # Inform the error microservice
        print('\n\n-----Invoking error microservice as order fails-----')
        invoke_http(error_URL, method="POST", json=food_result)
  
        print("Food status ({:d}) sent to the error microservice:".format(
            code), food_result)

    # 7. Return error
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


################## END OF SCENARIO 1 ####################




####################### START OF SCENARIO 3 ############################
# to view all posts in forum
# input: nth
# output: get all posts in json object with key forum:
@app.route("/posts", methods=['GET'])
def get_forum_posts():
    result = invoke_http(forum_URL, method='GET')
    if result:
        return jsonify(result), result["code"]  

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "no posts to return"}), 400

# show all forum posts 
def get_posts():

    print('\n-----Invoking forum microservice-----')
    forum_result = invoke_http(forum_URL, method='GET')
    print('forum_result:', forum_result)

    # Check the food result; if a failure, send it to the error microservice.
    code = forum_result["code"]
    if code not in range(200, 300):

    # # Inform the error microservice
    #     print('\n\n-----Invoking error microservice as order fails-----')
    #     invoke_http(error_URL, method="POST", json=forum_result)
  
    #     print("Forum status ({:d}) sent to the error microservice:".format(
    #         code), forum_result)

    # 7. Return error
        return {
            "code": 500,
            "data": {"forum_result": forum_result},
            "message": "Retrieve forum failure sent for error handling."
        }
    
    return {
        "code": 201,
        "data": {
            "forum_result": forum_result
        }
    }

# to create a post in forum
# input: comment, commentor_username, datetime, post_id
# output: get all posts in json object with key forum:
@app.route("/create_post", methods=['POST'])
def create_forum_post():
    if request.is_json:
        try:
            post_details = request.get_json()
            print("\nReceived post details in JSON:", post_details)

            # do the actual work
            result = create_post(post_details)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "forum_management.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


# create forum post function
def create_post(post_details):

    print('\n-----Invoking forum microservice-----')
    
    # url = create_forum_URL + '/create/' + str(post_details['post_id'])
    url = create_forum_URL + '/create'

    forum_result = invoke_http(url, method='POST', json=post_details)
    print('forum_result:', forum_result)

    # Check the food result; if a failure, send it to the error microservice.
    code = forum_result["code"]
    if code not in range(200, 300):

    # # Inform the error microservice
    #     print('\n\n-----Invoking error microservice as order fails-----')
    #     invoke_http(error_URL, method="POST", json=forum_result)
  
    #     print("Forum status ({:d}) sent to the error microservice:".format(
    #         code), forum_result)

    # 7. Return error
        return {
            "code": 500,
            "data": {"forum_result": forum_result},
            "message": "Retrieve forum failure sent for error handling."
        }
    
    return {
        "code": 201,
        "data": {
            "forum_result": forum_result
        }
    }


####################### END OF SCENARIO 3 ####################

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.

from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
from invokes import invoke_http
from invoke_activity import activity_log
app = Flask(__name__)
CORS(app)

forum_URL = 'http://localhost:1113/all'
create_forum_URL = 'http://localhost:1113'

'''

Function: display all posts in forum + with comments

Input: nothing

Output: 

return {
        "code": 201,
        "data": {
            "forum_result": 
                {
                "code": 200,
                "data": {
                    "forum": [forum.json() for forum in forum_list]
                }
            }
        }
    }
    
'''

@app.route("/posts", methods=['GET'])
def get_forum_posts():

    result = invoke_http(forum_URL, method='GET')
    activity_log("forum_info") #to put in activity log
    code = result["code"]
    if code not in range(200, 300):
        activity_log("forum_info_error")
        return {
            "code": 500,
            "data": {"forum_result": result},
            "message": "Retrieve forum failure sent for error handling."
        }
    
    return {
        "code": 201,
        "data": {
            "forum_result": result
        }
    }


'''

Function: to create a post in forum

Input: post details

Output: 

return jsonify(result), result["code"]

and result is 

return {
        "code": 201,
        "data": {
            "forum_result": 
                 {
                    "code": 201,
                    "data": 
                        {
                            'forum_id': forum_id,
                            'commentor_username': commentor_username,
                            'comment': comment,
                            'datetime': datetime
                        },
                    "message": "Post created successfully."
                }
        }
    }
    
'''
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
                "message": "manage_forum.py internal error: " + ex_str
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
    activity_log("forum_info") #to put in activity log
    print('forum_result:', forum_result)

    # Check the food result; if a failure, send it to the error microservice.
    code = forum_result["code"]
    if code not in range(200, 300):
        activity_log("forum_info_error")
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


'''
Function: create comments

Input: {
    forum_id: <int>,
    commentor_username: <string>,
    comment: <string>,
    datetime: <string>
}

Output: 

return jsonify(result), result["code"]

and result is 

return {
        "code": 201,
        "data": {
            "forum_result": 
                 {
                    "code": 201,
                    "data": 
                        {
                            'forum_id': forum_id,
                            'commentor_username': commentor_username,
                            'comment': comment,
                            'datetime': datetime
                        },
                    "message": "Post created successfully."
                }
        }
    }
'''

@app.route("/create_comment", methods=['POST'])
def create_comment():
    # Breaks if no json given
    if not request.is_json:
        print("Invalid parameter (no JSON given)")

        return jsonify({
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 400
    
    # If json given
    try:
        print("[LOOK HERE] Valid JSON passed, running create_comment()")
        comment_details = request.get_json()
        # print("\nReceived post details in JSON:", comment_details)

        # do the actual work
        result = push_new_comment(comment_details)

        return jsonify(result['data']), result["code"]

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
    
def push_new_comment(comment_details):
    print("push_new_comment(", comment_details, '"')

    url = create_forum_URL + '/create_comment'

    create_comment_result = invoke_http(url, method='POST', json = comment_details)
    activity_log("forum") #to put in activity log

    # If a failure, send it to the error microservice
    code = create_comment_result["code"]
    
    if code not in range(200, 300):
        # 7. Return error
        return {
            "code": 500,
            "data": create_comment_result,
            "message": "Retrieve forum failure sent for error handling."
        }
    else:
        return {
            "code": 201,
            "data": create_comment_result,
        }

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for managing forum posts...")
    app.run( port=5103, debug=True)
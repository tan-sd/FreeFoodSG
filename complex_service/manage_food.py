from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
from invokes import invoke_http
from invoke_activity import activity_log
app = Flask(__name__)
CORS(app)

create_post_URL = 'http://localhost:1112/create_post'

'''DOCUMENTATION HERE
User posts a new food post
input(json): 
{
    post_id = type int
    username = type varchar
    post_name = type varchar
    latitude = type float, precision 6
    longitude = type float, precision 6
    address = type varchar
    description = type varchar
    is_available = type bit or integer, 0 is false, 1 is true
    end_time = type varchar, in YYYY-MM-DD HH:MM:SS format
}
output(json):
{
    code: type int <- tells you the server code, 404 if error
    msg: details of the post if successful
}

'''
@app.route("/post", methods=['POST'])
def post_food():
    print('\n-----Invoking food_info microservice-----')

    if request.is_json:
        try:
            post_result = invoke_http(create_post_URL, method='POST', json=request.json)
            print('Post status:', post_result)
            code = post_result["code"]
            # CHECK OUTPUT
            # print(jsonify(post_result), post_result["code"])
            # return jsonify(post_result), post_result["code"]
        
            if code not in range(200, 300):

                activity_log("food_info error")
                return {
                    "code": 500,
                    "data": {"post_result": post_result},
                    "message": "Error creating post."
                }
            
            print("Food post created successfully!")
            activity_log("food_info")
            return {
                "code": 201,
                "data": {
                    "Post_result": post_result,
                }
            }
        
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            activity_log("food_info error")
            return jsonify({
                "code": 500,
                "message": "manage_food.py internal error: " + ex_str
            }), 500
    
    activity_log("post food is not json error")
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400
    

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for managing food posts...")
    app.run(port=5102, debug=True)
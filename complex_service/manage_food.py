from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from invokes import invoke_http
from invoke_activity import activity_log
app = Flask(__name__)
CORS(app)

create_post_URL = 'http://localhost:1112/create_post'

'''DOCUMENTATION HERE
User posts a new post
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
    post_result = invoke_http(create_post_URL, method='POST', json=request.json)
    activity_log("food_info")
    print('Post status:', post_result)
    return {
        "code": 201,
        "data": {
            "post_status": post_result
        }
    }

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for managing food posts...")
    app.run(port=5102, debug=True)
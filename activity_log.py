import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
from datetime import datetime

'''
This is activity_log microservice
It only has one function which is to add to the activity_log database
Ideal input: JSON of log information, which is either ms invoked, or ms error, or function error e.g.
    {
        "log_info" : "food_info"
    }
    if error:
    {
        "log_info" : "food_info_error"
    }
Output: None, this is a microservice which does not return any information
'''
# INITIALISING APP
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# if os.name == "nt":
#     connection = 'mysql+mysqlconnector://root@localhost:3306/activity_db'
# else:
#     connection = 'mysql+mysqlconnector://root:root@localhost:3306/activity_db'

# if (os.environ.get('dbURL')):
#     connection = os.environ.get('dbURL')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@host.docker.internal:3306/activity_db'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

# DECLARING TABLE
class activity_table(db.Model):
    __tablename__ = 'activity_table'
    log_id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    log_info = db.Column(db.VARCHAR(64), nullable=False)
    
    def __init__(self, log_id, created, log_info):
        self.log_id = log_id
        self.created = created
        self.log_info = log_info

    def json(self):
        log = {
            'log_id': self.log_id,
            'created': self.created,
            'log_info': self.log_info,
        }
        return log

@app.route("/create_log", methods=['POST'])
def create_log():
    '''
    this is the overarching function which creates a log and adds into database
    input: {"ms_invoked": "microservice_name"} OR
    input: {"ms_invoked": "microservice_name_error"}
    output: technically none 
    '''
    #check if not json
    if not request.is_json:
        data = request.get_data()
        print("Received an invalid log")
        print(data)
        print()

    #if json, try adding
    else:
        data = request.get_json()
        print("Recording log into database...")

        #if successful add
        if add_to_db(data) == True:
            print("Log added successfully!")
            return jsonify({"code": 200, "data": data}), 200
        
        else:
            print("Error adding log into database: ")
            print(add_to_db(data))
            return add_to_db(data)

def add_to_db(data):
    '''
    this function adds a log to the database for create_log app.route
    input: log json
    output: true if successful, json error description if failed
    '''   
    data["log_id"] = get_log_id()
    data["created"] = datetime.now() 

    try:
        log = activity_table(**data)
        db.session.add(log)
        db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "code":500,
                "message": "System Error Message: " + str(e)
            }
        ), 500
    
    return True

def get_log_id():
    '''
    this function checks the last id of the table and creates a new id for the incoming log
    input: nothing
    output: log_id of the last db entry + 1
    '''
    log_id = activity_table.query.order_by(activity_table.log_id.desc()).first().log_id
    return log_id + 1

if __name__ == '__main__':
    print("This microservice: " + os.path.basename(__file__) + ", records logs.")
    app.run(host="0.0.0.0", port=1120, debug=True)
# api.py
# Rest API to Select, add, update, delete Employee
# to Run use > flask run
#
#
from flask_cors import CORS, cross_origin
from flask import Flask, request
import time
import json
import logging

app = Flask(__name__)
CORS(app, support_credentials=True)

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   return response


@app.route('/')
def home():
    return '''
    <h1>API List</h1>
    <p>http://127.0.0.1:5000/time</p>
    <p>http://127.0.0.1:5000/api/v1/emp/all</p>
    <p>http://127.0.0.1:5000/update_emp</p>
    <p>http://127.0.0.1:5000/delete_emp</p>
    <p>http://127.0.0.1:5000/get_todo</p>
    <p>http://127.0.0.1:5000/update_todo</p>
    <p>http://127.0.0.1:5000/delete_todo</p>
    '''


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/api/v1/emp/<string:id>', methods=['GET'])
def get_emp(id=None):
    
    data = read_json_data(json_name="emp")
    logging.info("Getting emp data for ID : %s" % id)

    data = data.get(id)

    logging.info("data = %s" % data)

    return data


@app.route('/api/v1/emp', methods=['GET', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def get_emp_all():
    logging.info("Getting all employee")
    data = read_json_data(json_name="emp")
    return data


@app.route('/api/v1/emp/<string:id>', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def update_emp(id):    
    """Update existing employee or Add new one if not exists
    curl -d "id=001&firstName=Rahul&lastName=patil&age=22&jobTitle=Engineer&dateJoined=2020-07-01&bio=DB&avatar=https://duck.com" -X POST http://127.0.0.1:5000/api/v1/emp/001
    curl -d "id=E001&name=Prashant&last_name=patil&location=mumbai" -X POST http://127.0.0.1:5000/api/v1/emp/E001
    """
    logging.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    logging.info("updating employee %s" % id)
    logging.info(json.loads(request.data))
    logging.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    data = read_json_data(json_name="emp")    
    emp_data = json.loads(request.data)

    ids = dict([(emp["id"], emp_pos) for emp_pos, emp in enumerate(data["employees"])])
    logging.info(".......Ids : %s" % ids)

    if id in ids:
        logging.info("Id exists at position %s, updating" % ids[id])
        data["employees"].pop(ids[id])
        data["employees"].insert(ids[id], emp_data)
    else:
        logging.info(".......Id Does not exists, Adding it")        
        data["employees"].append(emp_data)

    update_json_data({"data": data}, json_name="emp")
    return data


@app.route('/api/v1/emp/<string:id>', methods=['DELETE', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def delete_emp(id):    
    logging.info("......deleting employee %s" % id)
    logging.info("......deleting employee %s" % id)
    data = read_json_data(json_name="emp")    
    ids = dict([(emp["id"], emp_pos) for emp_pos, emp in enumerate(data["employees"])])
    removed_emp = data["employees"].pop(ids[id])
    logging.info("......deleting employee %s" % removed_emp)
    update_json_data({"data": data}, json_name="emp")
    return data


@app.route('/api/v1/emp/<string:id>/todo', methods=['GET', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def get_todo(id=None):
    
    data = read_json_data(json_name="todo")
    logging.info("Getting toto data for ID : %s" % id)

    data = data.get(id)

    logging.info("data = %s" % data)
    return {"todo": data}

@app.route('/api/v1/todo', methods=['GET', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def get_todo_all():
    
    data = read_json_data(json_name="todo")    
    logging.info("data = %s" % data)
    return data


@app.route('/api/v1/emp/<string:id>/todo', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def update_todo(id):    
    """Update existing employee or Add new one if not exists
    curl -d "id=001&name=Rahul&last_name=patil&location=mumbai" -X POST http://127.0.0.1:5000/api/v1/emp/001
    curl -d "id=E001&name=Prashant&last_name=patil&location=mumbai" -X POST http://127.0.0.1:5000/api/v1/emp/E001
    """
    logging.info("updating employee %s" % id)
    data = read_json_data(json_name="todo")
    
    todo_data = json.loads(request.data)

    data[id] = todo_data

    update_json_data({"data": data}, json_name="todo")
    return data


@app.route('/api/v1/emp/<string:id>/todo/<string:todoid>', methods=['DELETE', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def delete_todo(id, todoid):    
    """Delete Todo
    """
    logging.info("........deleting to do for empid %s - todoid %s" % (id, todoid))
    data = read_json_data(json_name="todo")    
    ids = dict([(todo["todoid"], todo_pos) for todo_pos, todo in enumerate(data[id])])    
    removed_todoid = data[id].pop(ids[todoid])
    logging.info(".....deleted todo %s" % removed_todoid)
    update_json_data({"data": data}, json_name="todo")
    return data



def update_json_data(data, json_name):
    with open("asset/%s.json" % json_name, "w") as json_file:
        logging.info("Data to be updated in json %s" % (json_name))
        json.dump(data, json_file)
        logging.info("Successfully changes Json")


def read_json_data(json_name):
    """Read Json data from file
    """
    data = {}
    logging.info("........Reading data from json for %s" % json_name)

    with open("asset/%s.json" % json_name) as emp:
        data = json.load(emp) 
        # logging.info("Data from json %s: %s" % (json_name, data))

    logging.info("........Reading data from json completed")
    return data.get("data")

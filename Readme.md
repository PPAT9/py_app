# py App
Flask API

# python venv venv
# venv\Scripts\activate
# pip install flask
# pip install flask_dotenv
# to resolve cros
# pip install flask_cors

# add in .flaskenv
# FLASK_APP=api.py
# FLASK_ENV=development

# to run the app run
flask run

# Get all employee
curl -X GET http://127.0.0.1:5000/api/v1/emp
<!-- {
  "E001": {"id": "E001", "last_name": "patil", "location": "mumbai", "name": "Prashant"},
  "E002": {"id": "E002", "last_name": "pant", "location": "NJ", "name": "Rishab"}
} -->

# Get Employee
curl -X GET http://127.0.0.1:5000/api/v1/emp/E001
<!-- {"id": "E001", "last_name": "patil", "location": "mumbai", "name": "Prashant"} -->


# update Employee
curl -d "id=001&name=Rahul&last_name=patil&location=mumbai" -X POST http://127.0.0.1:5000/api/v1/emp/001

<!-- {
  "001": {"id": "001", "last_name": "patil", "location": "mumbai", "name": "Rahul"},
  "002": {"id": "002", "last_name": "pant", "location": "NJ", "name": "Rishab"}
} -->

# Delete Employee
$ curl  -X DELETE http://127.0.0.1:5000/api/v1/emp/E001
 
<!-- {"E002": {"id": "E002", "last_name": "pant", "location": "NJ", "name": "Rishab"}} -->

# Add Employee
$ curl -d "id=E001&name=Prashant&last_name=patil&location=mumbai" -X POST http://127.0.0.1:5000/api/v1/emp/E001
<!-- {
  "E001": {"id": "E001", "last_name": "patil", "location": "mumbai", "name": "Prashant"},
  "E002": {"id": "E002", "last_name": "pant", "location": "NJ", "name": "Rishab"}
} -->


# Get TODO
curl -X GET http://127.0.0.1:5000/api/v1/emp/E001/todo
<!-- {"data": {"001": {"desc": "create flask api"},"002": {"desc": "create React App"}}} -->

# Update TOTO
curl -H 'Content-Type: application/json' -X POST -d '{"data": {"001": {"desc": "create flask api"},"002": {"desc": "create React App"}}}' http://127.0.0.1:5000/api/v1/emp/E001/todo
<!-- {"E001": {"data": {"001": {"desc": "create flask api"},"002": {"desc": "create React App"}}}} -->

# Delete Todo
curl  -X DELETE http://127.0.0.1:5000/api/v1/emp/E002/todo
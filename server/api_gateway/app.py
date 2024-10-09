from flask import Flask, jsonify, request, make_response
import requests

app = Flask(__name__)

USERS_SERVICE = "http://users_service:1000"
ROOMS_SERVICE = "http://rooms_service:2000"
TASKS_SERVICE = "http://tasks_service:3000"
KEYS_SERVICE = "http://keys_service:4000"

#--Users--

#Get users or add an user
@app.route("/users", methods=["POST", "GET"])
def users():
    if request.method == "POST":
        data = request.get_json()
        response = requests.post(f"{USERS_SERVICE}/users", json=data)
    else:
        response = requests.get(f"{USERS_SERVICE}/users")
    return make_response(jsonify(response.json()), response.status_code)

#Get user by username
@app.route("/user/<string:username>", methods=["GET"])
def username(username):
    response = requests.get(f"{USERS_SERVICE}/user/{username}")
    return make_response(jsonify(response.json()), response.status_code)

#Get, edit or delete a user by id
@app.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def user(user_id):
    if request.method == "GET":
        response = requests.get(f"{USERS_SERVICE}/users/{user_id}")
    elif request.method == "PUT":
        data = request.get_json()
        response = requests.put(f"{USERS_SERVICE}/users/{user_id}", json=data)
    else:
        response = requests.delete(f"{USERS_SERVICE}/users/{user_id}")
    return make_response(jsonify(response.json()), response.status_code)

#All room with the mentioned user
@app.route("/users/<int:user_id>/rooms", methods=["GET"])
def get_user_rooms(user_id):
    response = requests.get(f"{KEYS_SERVICE}/users_rooms/user/{user_id}")
    return make_response(jsonify(response.json()), response.status_code)

#All tasks of the mentioned user
@app.route("/users/<int:user_id>/tasks", methods=["GET"])
def get_user_tasks(user_id):
    response = requests.get(f"{TASKS_SERVICE}/tasks/user/{user_id}")
    return make_response(jsonify(response.json()), response.status_code)

#--Rooms--

#Get rooms or add a room
@app.route("/rooms", methods=["GET", "POST"])
def rooms():
    if request.method == "GET":
        response = requests.get(f"{ROOMS_SERVICE}/rooms")
    else:
        data = request.get_json()
        response = requests.post(f"{ROOMS_SERVICE}/rooms", json=data)
    return make_response(jsonify(response.json()), response.status_code)

#Get room by code
@app.route("/rooms/<string:code>", methods=["GET"])
def code(code):
    response = requests.get(f"{ROOMS_SERVICE}/rooms/code/{code}")
    return make_response(jsonify(response.json()), response.status_code)

#Get or delete specify room
@app.route("/rooms/<int:room_id>", methods=["GET", "DELETE"])
def room(room_id):
    if request.method == "GET":
        response = requests.get(f"{ROOMS_SERVICE}/rooms/{room_id}")
    else:
        response = requests.delete(f"{ROOMS_SERVICE}/rooms/{room_id}")
    return make_response(jsonify(response.json()), response.status_code)

#All users in the room
@app.route("/rooms/<int:room_id>/users", methods=["GET"])
def get_room_users(room_id):
    response = requests.get(f"{KEYS_SERVICE}/users_rooms/room/{room_id}")
    return make_response(jsonify(response.json()), response.status_code)

#All tasks in the room
@app.route("/rooms/<int:room_id>/tasks", methods=["GET"])
def get_room_tasks(room_id):
    response = requests.get(f"{TASKS_SERVICE}/tasks/room/{room_id}")
    return make_response(jsonify(response.json()), response.status_code)

#Join user to the room
@app.route("/rooms/join", methods=["POST"])
def join():
    data=request.get_json()
    response = requests.post(f"{KEYS_SERVICE}/users_rooms", json=data)
    return make_response(jsonify(response.json()), response.status_code)

#Remove user from the room
@app.route("/rooms/remove", methods=["DELETE"])
def remove():
    data = request.get_json()
    response = requests.delete(f"{KEYS_SERVICE}/users_rooms", json=data)
    return make_response(jsonify(response.json()), response.status_code)

#--Tasks--

#Get all tasks or create new
@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "POST":
        data = request.get_json()
        response = requests.post(f"{TASKS_SERVICE}/tasks", json=data)
    else:
        response = requests.get(f"{TASKS_SERVICE}/tasks")
    return make_response(jsonify(response.json()), response.status_code)

#Get, edit or delete mentioned task
@app.route("/tasks/<int:task_id>", methods=["GET", "POST", "DELETE"])
def task(task_id):
    if request.method == "GET":
        response = requests.get(f"{TASKS_SERVICE}/tasks/{task_id}")
    elif request.method == "PUT":
        data = request.get_json()
        response = requests.put(f"{TASKS_SERVICE}/tasks/{task_id}", json=data)
    else:
        response = requests.delete(f"{TASKS_SERVICE}/tasks/{task_id}")
    return make_response(jsonify(response.json()), response.status_code)
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

USERS_SERVICE_URL = "http://users_service:5000"
ROOMS_SERVICE_URL = "http://rooms_service:5000"
TASKS_SERVICE_URL = "http://tasks_service:5000"


@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the TaskSync API Gateway!"
    }), 200


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        response = requests.get(f"{USERS_SERVICE_URL}/users")
    elif request.method == 'POST':
        data = request.json
        response = requests.post(f"{USERS_SERVICE_URL}/users", json=data)
    return jsonify(response.json()), response.status_code


@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(id):
    if request.method == 'GET':
        response = requests.get(f"{USERS_SERVICE_URL}/users/{id}")
    elif request.method == 'PUT':
        data = request.json
        response = requests.put(f"{USERS_SERVICE_URL}/users/{id}", json=data)
    elif request.method == 'DELETE':
        response = requests.delete(f"{USERS_SERVICE_URL}/users/{id}")
    return jsonify(response.json()), response.status_code


@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    if request.method == 'GET':
        response = requests.get(f"{ROOMS_SERVICE_URL}/rooms")
    elif request.method == 'POST':
        data = request.json
        response = requests.post(f"{ROOMS_SERVICE_URL}/rooms", json=data)
    return jsonify(response.json()), response.status_code


@app.route('/rooms/<int:id>', methods=['GET', 'DELETE'])
def room_detail(id):
    if request.method == 'GET':
        response = requests.get(f"{ROOMS_SERVICE_URL}/rooms/{id}")
    elif request.method == 'DELETE':
        response = requests.delete(f"{ROOMS_SERVICE_URL}/rooms/{id}")
    return jsonify(response.json()), response.status_code


@app.route('/rooms/<int:room_id>/users', methods=['POST'])
def add_user_to_room(room_id):
    data = request.json
    response = requests.post(f"{ROOMS_SERVICE_URL}/rooms/{room_id}/users", json=data)
    return jsonify(response.json()), response.status_code


@app.route('/rooms/<int:room_id>/users/<int:user_id>', methods=['DELETE'])
def remove_user_from_room(room_id, user_id):
    response = requests.delete(f"{ROOMS_SERVICE_URL}/rooms/{room_id}/users/{user_id}")
    return jsonify(response.json()), response.status_code


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        response = requests.get(f"{TASKS_SERVICE_URL}/tasks")
    elif request.method == 'POST':
        data = request.json
        response = requests.post(f"{TASKS_SERVICE_URL}/tasks", json=data)
    return jsonify(response.json()), response.status_code


@app.route('/tasks/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def task_detail(id):
    if request.method == 'GET':
        response = requests.get(f"{TASKS_SERVICE_URL}/tasks/{id}")
    elif request.method == 'PUT':
        data = request.json
        response = requests.put(f"{TASKS_SERVICE_URL}/tasks/{id}", json=data)
    elif request.method == 'DELETE':
        response = requests.delete(f"{TASKS_SERVICE_URL}/tasks/{id}")
    return jsonify(response.json()), response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

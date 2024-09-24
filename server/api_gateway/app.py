from flask import Flask, jsonify
from flask_caching import Cache
import requests

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})

USERS_SERVICE_URL = "http://users_service:5000/"
ROOMS_SERVICE_URL = "http://rooms_service:5000/"
TASKS_SERVICE_URL = "http://tasks_service:5000/"

@app.route('/')
@cache.cached(timeout=60)
def index():
    users_response = requests.get(USERS_SERVICE_URL)
    rooms_response = requests.get(ROOMS_SERVICE_URL)
    tasks_response = requests.get(TASKS_SERVICE_URL)

    if users_response.status_code == 200 and rooms_response.status_code == 200 and tasks_response.status_code == 200:
        users_data = users_response.json()
        rooms_data = rooms_response.json()
        tasks_data = tasks_response.json()

        return jsonify({
            "users": users_data,
            "rooms": rooms_data,
            "tasks": tasks_data
        })
    else:
        return jsonify({'error': 'Unable to fetch data from services.'}), 500

@app.route('/rooms', methods=["GET"])
@cache.cached(timeout=60)
def get_rooms():
    response = requests.get(ROOMS_SERVICE_URL)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Unable to fetch rooms.'}), 500

@app.route('/tasks', methods=['GET'])
@cache.cached(timeout=60)
def get_tasks():
    response = requests.get(TASKS_SERVICE_URL)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Unable to fetch tasks.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

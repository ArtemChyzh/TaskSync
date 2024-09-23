from flask import Flask, jsonify
from flask_caching import Cache
import requests

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})

ROOMS_SERVICE_URL = "http://rooms_service:5000/"
TASKS_SERVICE_URL = "http://tasks_service:5000/"

@app.route('/')
@cache.cached(timeout=60)
def index():
    rooms_response = requests.get(ROOMS_SERVICE_URL)
    tasks_response = requests.get(TASKS_SERVICE_URL)

    if rooms_response.status_code == 200 and tasks_response.status_code == 200:
        return rooms_response.json()["room"] + tasks_response.json()["task"]
    else:
        return jsonify({'error': 'Unable to fetch data from services.'}), 500

@app.route('/rooms', methods=["GET"])
@cache.cached(timeout=60)
def get_rooms():
    pass

@app.route('/tasks', methods=['GET'])
@cache.cached(timeout=60)
def get_tasks():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

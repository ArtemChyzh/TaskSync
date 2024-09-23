from flask import Flask

app = Flask(__name__)

ROOMS_SERVICE_URL = "http://rooms_service:5000/"
TASKS_SERVICE_URL = "http://tasks_service:5000/"

if __name__ == '__main__':
    app.run()
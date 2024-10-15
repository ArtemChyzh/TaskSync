from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import check_password_hash
import requests

USERS_SERVICE = "http://user_service:1000"

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secretkey"
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not all(k in data for k in ("username", "password")):
        return make_response(jsonify({"error": "Invalid data. 'username' and 'password' are required."}), 422)

    username = data["username"]
    password = data["password"]

    try:
        response = requests.get(f"{USERS_SERVICE}/user/{username}")
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            return make_response(jsonify({"error": "User is not found."}), 404)
        else:
            return make_response(jsonify({"error": f"Users service returned error: {str(err)}"}), 500)

    user_data = response.json()
    hash = user_data.get("password_hash")

    if not check_password_hash(hash, password):
        return make_response(jsonify({"error": "Password is wrong."}), 401)

    token = create_access_token(identity=username)
    return make_response(jsonify({"token": token}), 200)
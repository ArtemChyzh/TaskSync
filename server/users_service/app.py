from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from os import environ
from werkzeug.security import generate_password_hash
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_USERS")
db = SQLAlchemy(app)

KEYS_SERVICE = "http://keys_service:4000"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash
        }

with app.app_context():
    db.create_all()

@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        if not all(k in data for k in ("username", "email", "password")):
            return make_response(jsonify({"error": "Invalid data. 'username', 'email' and 'password' are required."}), 422)
        user = User.query.filter(or_(User.username==data["username"], User.email==data["email"])).first()
        if user:
            return make_response(jsonify({"error": "User already exists. 'username' and 'email' must be unique."}), 409)
        
        new_user = User(
            username=data["username"],
            email=data["email"],
            password_hash=generate_password_hash(data["password"])
        )
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"message": "User created successfully.", "user_id": new_user.id}), 201)
    
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)
        
@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/users/<int:id>", methods=["GET"])
def get_user_by_id(id):
    try:
        user = User.query.get(id)
        if user:
            return make_response(jsonify({"user": user.json()}), 200)
        return make_response(jsonify({"error": "User is not found."}), 404)
    
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/user/<string:username>", methods=["GET"])
def get_user_by_username(username):
    try:
        user = User.query.filter_by(username=username).first()
        if user:
            return make_response(jsonify({"user": user.json()}), 200)
        return make_response(jsonify({"error": "User is not found."}), 404)
    
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return make_response(jsonify({"error": "User is not found."}), 404)
        
        data = request.get_json()
        if "username" in data: user.username = data["username"]
        if "email" in data: user.email = data["email"]
        if "password" in data: user.password_hash = generate_password_hash(data["password"])
            
        db.session.commit()
        return make_response(jsonify({"message": "User updated successfully."}), 200)
        
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return make_response(jsonify({"error": "User is not found."}), 404)
            
        with db.session.begin_nested():
            db.session.delete(user)
            response =  requests.delete(f"{KEYS_SERVICE}/users_rooms/user/{id}")
            if response.status_code < 300 and response.status_code >= 200:
                return make_response(jsonify({"message": "User deleted successfully."}), 204)
            else:
                raise Exception(f"Error from KEYS_SERVICE: {response.json()}")      
    
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}))
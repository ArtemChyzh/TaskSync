from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://username:password@db_users/users_db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    users_list = [{
        "id": user.id,
        "username": user.username
    } for user in users]
    try: return jsonify(users_list)
    except Exception as e: return jsonify({"error": f"{str(e)} in users_service"}), 500

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id: int):
    user = User.query.get(id)
    if not user: return jsonify({ "error": "User not found" }), 404
    try:
        return jsonify({
            "id": user.id,
            "username": user.username,
            "password_hash": user.password_hash
        }), 200
    except Exception as e: return jsonify({ "error": str(e), "service": "users" }), 500

@app.route("users/<string:username>", methods=["GET"])
def get_user(username: str):
    user = User.query.filter_by(username=username).first()
    if not user: return jsonify({ "error": "User not found" }), 404
    try:
        return jsonify({
            "id": user.id,
            "username": user.username,
            "password_hash": user.password_hash
        }), 200
    except Exception as e:
        return jsonify({"error": str(e), "service": "users"}), 500

@app.route("users/<int:id>", methods=["DELETE"])
def delete_user(id: int):
    user = User.query.get(id)
    if not user: return jsonify({ "error": "User not found" }), 404
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({ "message": "User deleted succesfully" }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e), "service": "users" }), 500

@app.route("users/<int:id>", methods=["PUT"])
def update_user(id: int):
    user = User.query.get(id)
    if not user: return jsonify({ "error": "User not found" }), 404
    data = request.get_json()
    if "username" in data: user.username = data["username"]
    if "password_hash" in data: user.password_hash = data["password_hash"]
    try:
        db.session.commit()
        return jsonify({" message": "User updated successfully" }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({ "error": str(e), "service": "users" }), 500
    
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if "username" not in data or "password" not in data:
        return jsonify({"error": "Invalid data was sent. 'username' and 'password' are required", "service": "users"}), 400
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 409
    try:
        hashed_password = generate_password_hash(password=data["password"])
        user = User(username=data["username"], password_hash=hashed_password)
        db.session.add(user)
        db.session.commit
        return jsonify({"message": "User created succesfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e), "service": "users"}), 500


if __name__ == "__main__":
    app.run(debug=True)
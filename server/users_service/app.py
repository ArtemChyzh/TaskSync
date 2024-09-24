from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
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
    return jsonify(users_list)

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id: int):
    user = User.query.get(id)
    if not user: return jsonify({ "error": "User not found" }), 404
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "password_hash": user.password_hash
    }), 200

@app.route("users/<string:username>", methods=["GET"])
def get_user(username: str):
    user = User.query.filter_by(username=username).first()
    if not user: return jsonify({ "error": "User not found" }), 404
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "password_hash": user.password_hash
    }), 200

@app.route("users/<int:id>", methods=["DELETE"])
def delete_user(id: int):
    user = User.query.get(id)
    if not user: return jsonify({ "error": "User not found" }), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({ "message": "User deleted succesfully" }), 200

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
        return jsonify({ "error": str(e) }), 500

if __name__ == "__main__":
    app.run(debug=True)
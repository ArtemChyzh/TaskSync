from flask import Flask, request, jsonify, make_response
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from os import environ

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_KEYS")
db = SQLAlchemy(app)

USERS_SERVICE = "http://user_service:1000"
ROOMS_SERVICE = "http://rooms_service:3000"

class UserRoom(db.Model):
    __tablename__ = "users_rooms"
    user_id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, primary_key=True)

    def json(self):
        return {
            "user_id": self.user_id,
            "room_id": self.room_id
        }
    
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def test():
    return make_response(jsonify({
        "message": "Test route"
    }), 200)

@app.route("/users_rooms", methods=["POST"])
def join_user():
    try:
        data=request.get_json()
        if "user_id" not in data or "room_id" not in data:
            return make_response(jsonify({"Invalid data. 'user_id' and 'room_id' are required"}), 422)
        relation = UserRoom.query.filter(and_(UserRoom.room_id==data["room_id"], UserRoom.user_id==data["user_id"])).first()
        if relation:
            return make_response(jsonify({"User is already joined."}), 409)
        user_response = requests.get(f"{USERS_SERVICE}/users/{data.get('user_id')}")
        if user_response.status_code == 404:
            UserRoom.query.filter_by(user_id=data["user_id"]).delete()
            db.session.commit()
            return make_response(jsonify({"error": "User not found."}), 404)
        room_response=requests.get(f"{ROOMS_SERVICE}/rooms/{data.get('room_id')}")
        if room_response.status_code == 404:
            UserRoom.query.filter_by(room_id=data["room_id"]).delete()
            db.session.commit()
            return make_response(jsonify({"error": "Room not found."}), 404)
        new_relaition = UserRoom(
            user_id=data["user_id"],
            room_id=data["room_id"]
        )
        db.session.add(new_relaition)
        db.session.commit()
        return make_response(jsonify({"message": "User joined successfully"}), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/users_rooms/room/<int:room_id>", methods=["GET"])
def get_relation_by_room(room_id:int):
    try:
        relations = UserRoom.query.filter_by(room_id=room_id).all()
        if not relations:
            return make_response(jsonify({"error": "No users in room."}), 404)
        users = [{"user_id": relation.user_id for relation in relations}]
        return make_response(jsonify(users), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/users_rooms/user/<int:user_id>", methods=["GET"])
def get_relation_by_user(user_id:int):
    try:
        relations = UserRoom.query.filter_by(user_id=user_id).all()
        rooms = [{"room_id": relation.room_id} for relation in relations]
        if rooms:
            return make_response(jsonify(rooms), 200)
        return make_response(jsonify({"error": "User is not found or has no rooms"}))
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/users_rooms", methods=["DELETE"])
def delete_relation():
    try:
        data = request.get_json()
        if "user_id" not in data or "room_id" not in data:
            return make_response(jsonify({"error": "Invalid data. 'user_id' and 'room_id' are required"}), 422)
        user_room = UserRoom.query.filter(and_(UserRoom.user_id==data["user_id"], UserRoom.room_id==data["room_id"])).first()
        if not user_room:
            return make_response(jsonify({"error": "Relation is not found."}), 404)
        db.session.delete(user_room)
        db.session.commit()

        remaining_users = UserRoom.query.filter_by(room_id=data["room_id"]).all()
        if not remaining_users:
            response = requests.delete(f"{ROOMS_SERVICE}/rooms/{data.get('room_id')}")
            if response.status_code < 300 and response.status_code >= 200:
                return make_response(jsonify({"message": "User removed and room deleted as it had no users"}))
            else:
                return make_response(jsonify(response.json()), response.status_code)
        return make_response(jsonify({"message": "User removed from room successfully"}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/users_rooms/user/<int:user_id>", methods=["DELETE"])
def delete_all_relations_for_user(user_id):
    try:
        deleted_count = UserRoom.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        if deleted_count > 0:
            return make_response(jsonify({"message": f"Deleted {deleted_count} relations for user {user_id}"}), 200)
        else:
            return make_response(jsonify({"message": "No relations found."}), 404)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/users_rooms/room/<int:room_id>", methods=["DELETE"])
def delete_all_relations_for_room(room_id):
    try:
        deleted_count = UserRoom.query.filter_by(room_id=room_id).delete()
        db.session.commit()

        if deleted_count > 0:
            return make_response(jsonify({"message": f"Deleted {deleted_count} relations for room {room_id}"}), 200)
        else:
            return make_response(jsonify({"message": "No relations found for this room"}), 404)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)
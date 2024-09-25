from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://username:password@db_rooms/rooms_db'
db = SQLAlchemy(app)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(9), nullable=False, unique=True)
    users = db.relationship('UserRoom', backref='room', lazy=True, cascade="all, delete-orphan")

class UserRoom(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, index=True)
    room_id = db.Column(db.Integer, db.ForeignKey(Room.id, ondelete="CASCADE"), primary_key=True, index=True)

@app.route('/rooms/<int:room_id>/users', methods=["POST"])
def add_user_to_room(room_id):
    data = request.get_json()
    if "user_id" not in data:
        return jsonify({"error": "Invalid data. 'user_id' is required"}), 400
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404
    user_room = UserRoom.query.filter_by(user_id=data["user_id"], room_id=room_id).first()
    if user_room:
        return jsonify({"error": "User is already in the room"}), 403
    try:
        new_user_room = UserRoom(user_id=data["user_id"], room_id=room_id)
        db.session.add(new_user_room)
        db.session.commit()
        return jsonify({"message": "User added to the room successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e), "service": "rooms"}), 500

@app.route('/rooms/<int:room_id>/users/<int:user_id>', methods=["DELETE"])
def remove_user_from_room(room_id, user_id):
    user_room = UserRoom.query.filter_by(user_id=user_id, room_id=room_id).first()
    if not user_room:
        return jsonify({"error": "User not found in the room"}), 404
    try:
        db.session.delete(user_room)
        db.session.commit()
        remaining_users = UserRoom.query.filter_by(room_id=room_id).count()
        if remaining_users == 0:
            room = Room.query.get(room_id)
            db.session.delete(room)
            db.session.commit()
        return jsonify({"message": "User removed from the room successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e), "service": "rooms"}), 500

@app.route('/rooms', methods=["GET"])
def get_rooms():
    rooms = Room.query.options(joinedload(Room.users)).all()
    result = []
    for room in rooms:
        user_ids = [user_room.user_id for user_room in room.users]
        result.append({
            'room_id': room.id,
            'code': room.code,
            'user_ids': user_ids
        })
    try:
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e), "service": "rooms"}), 500

@app.route('/rooms/<int:id>', methods=["GET"])
def get_room(id: int):
    room = Room.query.options(joinedload(Room.users)).get(id)
    if not room:
        return jsonify({"error": "Room not found"}), 404
    user_ids = [user_room.user_id for user_room in room.users]
    try:
        return jsonify({
            "room_id": room.id,
            "code": room.code,
            "user_ids": user_ids
        }), 200
    except Exception as e:
        return jsonify({"error": str(e), "service": "rooms"}), 500

@app.route("/rooms", methods=["POST"])
def create_room():
    data = request.get_json()
    if "user_id" not in data or "code" not in data:
        return jsonify({"error": "Invalid data. 'user_id' and 'code' are required"}), 400
    if Room.query.filter_by(code=data["code"]).first():
        return jsonify({"error": "Room with this code already exists"}), 403
    try:
        room = Room(code=data["code"])
        db.session.add(room)
        db.session.flush()
        user_room = UserRoom(user_id=data["user_id"], room_id=room.id)
        db.session.add(user_room)
        db.session.commit()
        return jsonify({"message": "Room created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e), "service": "rooms"}), 500

if __name__ == "__main__":
    app.run(debug=True)

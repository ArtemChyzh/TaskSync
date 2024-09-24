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
    users = db.relationship('UserRoom', backref='room', lazy=True)

class UserRoom(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, index=True)
    room_id = db.Column(db.Integer, db.ForeignKey(Room.id), primary_key=True, index=True)

@app.route('/', methods=["GET"])
def test():
    return jsonify({
        "room": "Hello, "
    })

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
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
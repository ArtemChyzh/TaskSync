from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://username:password@db_rooms/rooms_db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(9), nullable=False, unique=True)
    users = db.relationship('UserRoom', backref='room', lazy=True)

class UserRoom(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True, index=True)
    room_id = db.Column(db.Integer, db.ForeignKey(Room.id), primary_key=True, index=True)
    user = db.relationship('User', backref='user_rooms')

if __name__ == "__main__":
    app.run()
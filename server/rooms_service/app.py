from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_ROOMS")
db = SQLAlchemy(app)

class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(4), nullable=False, unique=True, index=True)
    title = db.Column(db.String(128), nullable=True)
    description = db.Column(db.String(4096), nullable=True)

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "code": self.code,
            "title": self.title,
            "description": self.description
        }

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def test():
    return make_response(jsonify({"message": "Test route"}), 200)
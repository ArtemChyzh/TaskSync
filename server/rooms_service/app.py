from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_ROOMS")
db = SQLAlchemy(app)

KEYS_SERVICE = "http://keys_service:4000"
CODE_SERVICE = "http://codes_service:200"

class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(6), nullable=False, unique=True, index=True)
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

@app.route("/rooms", methods=["POST"])
def create_room():
    try:
        data = request.get_json()
        
        if "user_id" not in data:
            return make_response(jsonify({"error": "Invalid data. 'user_id' is required"}), 422)
        
        response = requests.get(f"{CODE_SERVICE}/code")
        if response.status_code != 200:
            return make_response(jsonify({"message": "Something went wrong when creating unique code. Try again later, please."}), 500)
        
        code = response.json().get("code")
        
        room = Room.query.filter_by(code=code).first()
        if room:
            return make_response(jsonify({"error": "Room already exists. 'code' must be unique"}), 409)
        
        new_room = Room(
            user_id=data["user_id"],
            code=code,
            title=data.get("title", code),  # Якщо назва не вказана, використовуємо код як заголовок
            description=data.get("description", "")
        )
        db.session.add(new_room)
        db.session.commit()
        
        return make_response(jsonify({"message": "Room created successfully.", "room_id": new_room.id}), 201)
    
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/rooms/<int:id>", methods=["GET"])
def get_room_by_id(id:int):
    try:
        room = Room.query.get(id)
        if room:
            return make_response(jsonify(room.json()), 200)
        return make_response(jsonify({"error": "Room is not found."}), 404)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/rooms/code/<string:code>", methods=["GET"])
def get_room_by_code(code:str):
    try:
        room = Room.query.filter_by(code=code).first()
        if room:
            return make_response(jsonify(room.json()), 200)
        return make_response(jsonify({"error": "Room is not found"}), 404)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/rooms/<int:id>", methods=["PUT"])
def update_room(id:int):
    try:
        room = Room.query.get(id)
        if not room:
            return make_response(jsonify({"error": "Room is not found."}), 404)
        data = request.get_json()
        if "title" in data: room.title=data["title"]
        if "description" in data: room.description=data["description"]
        db.session.commit()
        return make_response(jsonify({"message": "Room updated successfully."}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/rooms/<int:id>", methods=["DELETE"])
def delete_room(id:int):
    try:
        room = Room.query.get(id)
        if not room:
            return make_response(jsonify({"error": "Room is not found."}), 404)
        
        db.session.delete(room)
        db.session.commit()
        
        try:
            response = requests.delete(f"{KEYS_SERVICE}/users_rooms/room/{id}")
            if response.status_code < 300 and response.status_code >= 200:
                return make_response(jsonify({"message": "Room deleted successfully."}), 204)
            else:
                error_message = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                return make_response(jsonify({"error": f"Room deleted, but failed to delete keys: {error_message}"}), response.status_code)
        except requests.RequestException as e:
            return make_response(jsonify({"error": f"Room deleted, but failed to communicate with keys service: {str(e)}"}), 500)
    
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/rooms/codes")
def get_codes():
    try:
        codes = db.session.query(Room.code).all()
        codes_list = [code[0] for code in codes]
        return make_response(jsonify(codes_list), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

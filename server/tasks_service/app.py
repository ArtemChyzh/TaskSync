from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import datetime, timezone, timedelta
from enum import Enum

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_TASKS")
db = SQLAlchemy(app)

class Status(Enum):
    pending = (1, "Pending.")
    in_progress = (2, "In progress...")
    completed= (3, "Completed!")

    def __new__(cls, value, text):
        obj = object.__new__(cls)
        obj._value_=value
        obj.text=text
        return obj

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(4096), nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc) + timedelta(days=7))
    status = db.Column(db.Enum(Status), nullable=False, default=Status.pending.value)

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
            "room_id": self.room_id,
            "deadline": self.deadline.isoformat(),
            "status": {
                "id": self.status.value,
                "text": self.status.text
            }
        }
    
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def test():
    return make_response(jsonify({
        "message": "Test route"
    }), 200)

@app.route("/tasks", methods=["POST"])
def create_task():
    try:
        data = request.get_json()
        if "title" not in data or "user_id" not in data or "room_id" not in data:
            return make_response(jsonify({"error": "Invalid data. 'title', 'user_id' and 'room_id' are required"}), 422)
        new_task = Task(
            title=data["title"],
            user_id=data["user_id"],
            room_id=data["room_id"],
            description=data.get("description", ""),
            deadline=data.get("deadline", (datetime.now(timezone.utc) + timedelta(days=7))),
            status=data.get("status", Status.pending.value)
        )
        db.session.add(new_task)
        db.session.commit()
        return make_response(jsonify({"message": "Task created successfully", "task_id": new_task.id}), 201)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        tasks = Task.query.all()
        return make_response(jsonify([task.json() for task in tasks]), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/tasks/<int:id>", methods=["GET"])
def get_task_by_id(id:int):
    try:
        task = Task.query.get(id)
        if task:
            return make_response(jsonify(task.json()), 200)
        return make_response(jsonify({"error": "Task is not found."}), 404)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/tasks/user/<int:user_id>", methods=["GET"])
def get_tasks_of_user(user_id:int):
    try:
        tasks = Task.query.filter_by(user_id=user_id)
        if tasks:
            return make_response(jsonify([task.json() for task in tasks]), 200)
        return make_response(jsonify({"error": "User is not found or has no tasks."}), 404)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}))
    
@app.route("/tasks/room/<int:room_id>", methods=["GET"])
def get_tasks_in_room(room_id:int):
    try:
        tasks = Task.query.filter_by(room_id=room_id)
        if tasks:
            return make_response(jsonify([task.json() for task in tasks]), 200)
        return make_response(jsonify({"error": "Room is not found or contains no tasks."}), 404)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}))
    
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id:int):
    try:
        task = Task.query.get(id)
        if task:
            data = request.get_json()
            if "title" in data: task.title=data["title"]
            if "user_id" in data: task.user_id=data["user_id"]
            if "room_id" in data: task.room_id=data["room_id"]
            if "description" in data: task.description=data["description"]
            if "deadline" in data: task.deadline=data["deadline"]
            if "status" in data: 
                status_value = data["status"]
                if status_value in [status.value for status in Status]:
                    task.status=Status(status_value)
                else:
                    return make_response(jsonify({"error": "Invalid status value. (1, 2, 3) are possible."}), 422)
            db.session.commit()
            return make_response(jsonify({"message": "Task updated successfully."}), 200)
        return make_response(jsonify({"error": "Task is not found."}), 404)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id:int):
    try:
        task = Task.query.get(id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return make_response(jsonify({"message": "Task deleted successfully."}), 204)
        return make_response(jsonify({"error": "Task is not found."}), 404)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
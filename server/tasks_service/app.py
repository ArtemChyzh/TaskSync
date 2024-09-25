from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os, enum, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://username:password@db_task/task_db'
db = SQLAlchemy(app)

class TaskStatus(enum.Enum):
    pending = "pending"
    in_progress = "in progress"
    completed = "completed"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.pending)
    deadline = db.Column(db.DateTime, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7))

@app.route('/tasks', methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    try:
        return jsonify([
            {
                'id': task.id,
                'user_id': task.user_id,
                'room_id': task.room_id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'deadline': task.deadline
            } for task in tasks
        ])
    except Exception as e: return jsonify({ "error": str(e), "service": "tasks" }), 500

@app.route('/tasks/<int:id>', methods=["GET"])
def get_task(id:int):
    task = Task.query.get(id)
    if not task: return jsonify({ "error": "Task not found" }), 404
    try:
        return jsonify({
            'id': task.id,
            'user_id': task.user_id,
            'room_id': task.room_id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'deadline': task.deadline
        })
    except Exception as e: return jsonify({ "error": str(e), "service": "tasks" }), 500

@app.route('/tasks', methods=["POST"])
def create_task():
    data = request.get_json()
    if ["user_id", "room_id", "title"] in data:
        return jsonify({"error": "Invalid data was sent. 'user_id', 'room_id', 'title' are required", "service": "tasks"})
    try:
        task = Task(user_id=data["user_id"], room_id=data["room_id"], title=data["title"])
        if "description" in data: task.description = data["description"]
        if "deadline" in data: task.deadline = data["deadline"]
        db.session.add(task)
        db.session.commit()
        return jsonify({"message": "Task created succesfully"}), 201
    except Exception as e:
        db.session.rollback
        return jsonify({"error": str(e), "service": "tasks"}), 500
    
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id: int):
    data = request.get_json()
    task = Task.query.get(id)
    if "title" in data: task.title = data["title"]
    if "description" in data: task.description = data["description"]
    if "status" in data: task.status = data["status"]
    if "deadline" in data: task.deadline = data["deadline"]
    try:
        db.session.commit()
        return jsonify({"message": "Task updated succesfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e), "service": "tasks"}), 500
    
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id: int):
    task = Task.query.get(id)
    if not task: return jsonify({"error": "Task not found"}), 404
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"mesage": "Task deleted succesfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e), "service": "tasks"}), 500

if __name__ == '__main__':
    app.run()
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os, enum

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
    description = db.Column(db.Text)
    status = db.Column(db.Enum(TaskStatus), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)

@app.route("/", methods=["GET"])
def test():
    return jsonify({
        "task": "world!"
    })

@app.route('/tasks', methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([
        {
            'id': task.id,
            'user_id': task.user_id,
            'room_id': task.room_id,
            'title': task.title,
            'description': task.description,
            'status': task.status
        } for task in tasks
    ])

if __name__ == '__main__':
    app.run()
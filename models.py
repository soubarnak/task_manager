from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.String(20), nullable=False, default="Medium")
    status = db.Column(db.String(20), default="Pending")  # Field for task status
    assigned_to = db.Column(db.String(50), nullable=False)  # Field for assignee

    def __repr__(self):
        return f'<Task {self.title}>'

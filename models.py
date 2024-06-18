from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# projects table
class Projects(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    manager_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)


# tasks table
class Tasks(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)


# workers table
class Workers(db.Model):
    __tablename__ = "workers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255))
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # password functions for auth.py
    def set_password(self, plaintext_password):
        self.password = generate_password_hash(plaintext_password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# files table
class Files(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(10))
    description = db.Column(db.Text)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)


# comments table
class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)


# status table
class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(255), nullable=False)

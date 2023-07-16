# models.py
from app import db, login_manager
from flask_login import UserMixin

# Модель пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(100))

# Модель задачи
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtasks = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
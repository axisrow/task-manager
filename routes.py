# routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from models import User, Task

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:  # если пользователь уже существует
            flash('Username already exists.')
            return redirect(url_for('signup'))

        new_user = User(username=username, password_hash=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login')) 

        login_user(user)
        return redirect(url_for('tasks'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/create_task', methods=['POST'])
@login_required
def create_task():
    title = request.form.get('title')
    subtasks = request.form.get('subtasks')
    new_task = Task(title=title, subtasks=subtasks, user_id=current_user.id)

    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('tasks'))

@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        title = request.form.get('title')
        subtasks = request.form.get('subtasks')

        new_task = Task(title=title, subtasks=subtasks, user_id=current_user.id)

        db.session.add(new_task)
        db.session.commit()

        flash('Task added successfully.')
        return redirect(url_for('tasks'))

    tasks = Task.query.filter_by(user_id=current_user.id)
    return render_template('tasks.html', tasks=tasks)
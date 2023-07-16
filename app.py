from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_login import logout_user
from werkzeug.security import generate_password_hash, check_password_hash

# Инициализируем SQLAlchemy вне функции create_app()
db = SQLAlchemy()

def create_app():
    # Инициализируем Flask приложение
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    # Инициализируем SQLAlchemy
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Инициализируем LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Функция загрузки пользователя
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

# Создаем Flask приложение
app = create_app()

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

# Создание всех таблиц в базе данных
with app.app_context():
    db.create_all()

# Инициализация LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

if __name__ == '__main__':
    app.run(debug=True)

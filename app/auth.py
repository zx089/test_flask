import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from app.models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        flash('Пожалуйста, проверьте правильность Ваших данных и попробуйте снова.')
        return redirect(url_for('auth.login'))

    user.last_login = datetime.datetime.now()
    db.session.commit()

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Извините, но данный адрес электронной почты уже зарегистрирован!')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email,
                    name=name,
                    password=generate_password_hash(password, method='sha256'),
                    created_on=datetime.datetime.now())

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('main.library'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

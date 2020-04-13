from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import SqlAlchemySessionInterface


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['REMEMBER_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_DURATION'] = 300
    app.config['DEBUG'] = False
    app.config['SECRET_KEY'] = 'test_app123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Извините, доступ есть только у авторизованных пользователей'
    login_manager.session_protection = "strong"

    db.init_app(app)
    login_manager.init_app(app)
    SqlAlchemySessionInterface(app, db, "sessions", "sess_")

    with app.app_context():
        from app.auth import auth as auth_blueprint
        from app.main import main as main_blueprint

        app.register_blueprint(auth_blueprint)
        app.register_blueprint(main_blueprint)

        db.create_all()

        return app

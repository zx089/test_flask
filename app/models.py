import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    posts = db.relationship('Post', backref='post', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    text = db.Column(db.String(200))
    is_deleted = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def as_dict(self):
        d_obj = {
            'id': self.id,
            'name': self.name,
            'text': self.text
        }
        return d_obj



from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class User(Base, UserMixin):
    ROLE_USER, ROLE_STAFF, ROLE_ADMIN = 10, 20, 30
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    job = db.Column(db.String(64))
    courses = db.relationship('Course', cascade='all, delete-orphan')

    def __repr__(self):
        return '<User: {}>'.format(self.name)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, haha):
        self._password = generate_password_hash(haha)

    def checkpassword(self, p):
        return check_password_hash(self._password, p)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN


class Course(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(256))
    image_url = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    author = db.relationship('User')
    chapters = db.relationship('Chapter', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Course: {}>'.format(self.name)


class Chapter(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(256))
    video_url = db.Column(db.String(256))
    video_duration = db.Column(db.String(32))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'))
    course = db.relationship('Course')

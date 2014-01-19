# -*- coding: utf-8 -*-

"""
flaskPage models.
"""
from passlib.apps import custom_app_context as pwd_context

from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=True)
    password = db.Column(db.String, nullable=False)   # The hashed password

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = pwd_context.encrypt(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password)

    def __repr__(self):
        return '<User "{username}">'.format(username=self.username)


class Submission(db.Model):
    """docstring for Submission"""

    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), unique=False, nullable=False)
    url = db.Column(db.String(399), unique=False, nullable=True)
    ups = db.Column(db.Integer, default=1)
    downs = db.Column(db.Integer, default=0)
    # comments=db.Column(db.Integer, default=0)
    # self_text=db.Column(db.String(5000), default=None)
    timestamp = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship(User)

    def __repr__(self):
        return '<Submission {id} "{title}"'.format(id=self.id, title=self.title)


class Vote(db.Model):
    __tablename__ = 'user_votes'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String, nullable=False)
    vote_value = db.Column(db.Integer)

    def __init__(self, user, submission_id, vote_value):
        self.user = user
        self.submission_id = submission_id
        self.vote_value = vote_value

    def __repr__(self):
        return "<Vote {vote_id} by {vote_user}".format(vote_id=self.id, vote_user=self.user)
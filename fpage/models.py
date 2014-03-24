# -*- coding: utf-8 -*-

"""
flaskPage models.
"""
from passlib.apps import custom_app_context as pwd_context

from flask.ext.sqlalchemy import SQLAlchemy

import datetime


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=True)
    password = db.Column(db.String, nullable=False)  # The hashed password

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
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), unique=False, nullable=False)
    url = db.Column(db.String(399), unique=False, nullable=True)
    ups = db.Column(db.Integer, default=1)
    downs = db.Column(db.Integer, default=0)
    # self_text=db.Column(db.String(5000), default=None)
    timestamp = db.Column(db.DateTime, nullable=False)
    author = db.Column(db.String, nullable=False)
    comment_count = db.Column(db.Integer, default=0)
    comments=db.relationship('Comment', backref='thread', lazy='dynamic')


    def post_comment(self, author, content,nested_limit, timestamp, parent_id=None):
        if parent_id:
            if parent_id.isdigit():
                parent=Comment.query.filter_by(id=int(parent_id)).first()
                if parent is None:
                    return False

                if parent.level>=nested_limit:
                    return "max depth exceeded"
            else:
                return False

            comment=Comment(self.id, author.username, content, timestamp, parent)
        else:
            comment=Comment(self.id, author.username, content, timestamp)
        self.comment_count+=1
        db.session.add(comment)
        db.session.commit()
        return True

    def get_comments(self):
        return self.comments.filter_by(level=0).all()


    def get_timestamp(self):
        return self.timestamp.isoformat()

    def __repr__(self):
        return '<Submission {id} "{title} >"'.format(id=self.id, title=self.title)


class ThreadVotes(db.Model):
    __tablename__ = 'thread_votes'

    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('submissions.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    vote_value = db.Column(db.Integer)

    def __init__(self, user, thread, value):
        self.user = user.id
        self.thread_id = thread.id
        self.vote_value = value

    def __repr__(self):
        return "<Thread Vote {vote_id} by user id {vote_user}>".format(vote_id=self.id,
                                                                       vote_user=self.user)

class CommentVotes(db.Model):
    __tablename__ = 'comment_votes'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    vote_value = db.Column(db.Integer)

    def __init__(self, user, comment, value):
        self.user=user.id
        self.comment_id=comment.id
        self.vote_value=value

    def __repr__(self):
        return "<Comment Vote {vote_id} by user id:{vote_user}>".format(vote_id=self.id,
                                                                        vote_user=self.user)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('submissions.id'))
    author = db.Column(db.String, nullable=False) #todo: rel to author
    content = db.Column(db.String, nullable=False)
    ups = db.Column(db.Integer, default=1)
    downs = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    children=db.relationship('Comment', backref=db.backref('parent',
                                            remote_side=[id]), lazy='dynamic')
    timestamp=db.Column(db.DateTime, nullable=False)
    level=db.Column(db.Integer, default=0)

    def __init__(self, thread_id, author, content, timestamp, parent=None):
        self.thread_id = thread_id
        self.author = author
        self.content = content
        self.timestamp=timestamp
        if parent is not None:
            self.parent_id = parent.id
            self.level=parent.level+1
        else:
            self.parent_id=None
            self.level=0

    def get_comments(self):
        return self.children.all()

    def get_indent(self):
            return "{}em".format(self.level*4.25)

    def get_timestamp(self):
        return self.timestamp.isoformat()

    def __repr__(self):
        return "<Comment {} >".format(self.id)
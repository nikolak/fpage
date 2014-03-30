# encoding: utf-8

import datetime as dt

from fpage.database import db, CRUDMixin


class Message(CRUDMixin, db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String, nullable=False)
    reciever = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    description =db.Column(db.String, nullable=False)
    thread_url=db.Column(db.String)

    def __init__(self, sender, reciever, content, description, thread_url):
        self.sender = sender
        self.reciever = reciever
        self.content = content
        self.timestamp = dt.datetime.now()
        self.description = description
        self.thread_url = thread_url
        

    @property
    def iso_time(self):
        return self.timestamp.isoformat()
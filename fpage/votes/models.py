# encoding: utf-8

from fpage.database import db, CRUDMixin


class ThreadVotes(CRUDMixin,db.Model):
    __tablename__ = 'thread_votes'

    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('submission.id'))
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    vote_value = db.Column(db.Integer)

    def __init__(self, user, thread, value):
        self.user = user.id
        self.thread_id = thread.id
        self.vote_value = value

    def __repr__(self):
        return "<Thread Vote {vote_id} by user id {vote_user}>".format(vote_id=self.id,
                                                                       vote_user=self.user)

class CommentVotes(CRUDMixin,db.Model):
    __tablename__ = 'comment_votes'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    vote_value = db.Column(db.Integer)

    def __init__(self, user, comment, value):
        self.user=user.id
        self.comment_id=comment.id
        self.vote_value=value

    def __repr__(self):
        return "<Comment Vote {vote_id} by user id:{vote_user}>".format(vote_id=self.id,
                                                                        vote_user=self.user)


# encoding: utf-8

from fpage.database import db, CRUDMixin

class Comment(CRUDMixin, db.Model):
    __tablename__ = 'comment'


    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('submission.id'))
    author = db.Column(db.String, nullable=False)  #todo: rel to author
    content = db.Column(db.String, nullable=False)
    ups = db.Column(db.Integer, default=1)
    downs = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    children = db.relationship('Comment', backref=db.backref('parent',
                                                             remote_side=[id]), lazy='dynamic')
    timestamp = db.Column(db.DateTime, nullable=False)
    level = db.Column(db.Integer, default=0)


    def __init__(self, thread_id, author, content, timestamp, parent=None):
        self.thread_id = thread_id
        self.author = author
        self.content = content
        self.timestamp = timestamp
        if parent is not None:
            self.parent_id = parent.id
            self.level = parent.level + 1
        else:
            self.parent_id = None
            self.level = 0


    def get_comments(self):
        return self.children.all()


    def get_timestamp(self):
        return self.timestamp.isoformat()


    def __repr__(self):
        return "<Comment {} >".format(self.id)
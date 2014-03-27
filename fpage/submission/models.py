# encoding: utf-8

from fpage.database import db, CRUDMixin
import fpage.comment.models

class Submission(CRUDMixin, db.Model):

    __tablename__ = 'submission'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), unique=False, nullable=False)
    url = db.Column(db.String(399), unique=False, nullable=True)
    ups = db.Column(db.Integer, default=1)
    downs = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, nullable=False)
    author = db.Column(db.String, nullable=False)
    comment_count = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='thread', lazy='dynamic')

    def __init__(self, title, url, timestamp, author):
        self.title = title
        self.url = url
        self.timestamp = timestamp
        self.author = author


    def post_comment(self, author, content, nested_limit, timestamp, parent_id=None):
        if parent_id:
            if parent_id.isdigit():
                parent = fpage.comment.models.Comment.query.filter_by(id=int(parent_id)).first()
                if parent is None:
                    return False

                if parent.level >= nested_limit:
                    return "max depth exceeded"
            else:
                return False

            comment = fpage.comment.models.Comment(self.id, author.username, content, timestamp, parent)
        else:
            comment = fpage.comment.models.Comment(self.id, author.username, content, timestamp)
        self.comment_count += 1
        db.session.add(comment)
        db.session.commit()
        return True


    def get_comments(self):
        return self.comments.filter_by(level=0).all()


    def get_timestamp(self):
        return self.timestamp.isoformat()


    def __repr__(self):
        return '<Submission {id} "{title} >"'.format(id=self.id, title=self.title)

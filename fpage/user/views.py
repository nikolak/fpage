# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

import fpage.user
import fpage.submission
import fpage.comment

blueprint = Blueprint("user", __name__, url_prefix='/user',
                      static_folder="../static")


@blueprint.route("/<username>", methods=['GET'])
def user(username):
    user = fpage.user.models.User.query.filter_by(username=username).first()
    if user is None:
        return render_template("404.html")
    else:
        return render_template("users/user.html",
                               user=user)

@blueprint.route("/<username>/submissions/", methods=['GET'])
@blueprint.route("/<username>/submissions/<int:page>", methods=['GET'])
def user_submissions(username, page=1):
    user = fpage.user.models.User.query.filter_by(username=username).first()
    if user is None:
        return render_template("404.html")
    else:
        submissions = fpage.submission.models.Submission.query.filter_by(author=user.username).all()
        return render_template("users/user_submissions.html",
                               submissions=submissions[(page * 25) - 25:page * 25],
                               user=user,
                               page=page)

@blueprint.route("/<username>/comments", methods=['GET'])
@blueprint.route("/<username>/comments/<int:page>", methods=['GET'])
def user_comments(username, page=1):
    user = fpage.user.models.User.query.filter_by(username=username).first()
    if user is None:
        return render_template("404.html")
    else:
        comments = fpage.comment.models.Comment.query.filter_by(author=user.username).all()
        return render_template("users/user_comments.html",
                               comments=comments[(page * 25) - 25:page * 25],
                               user=user,
                               page=page)
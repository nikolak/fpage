# -*- coding: utf-8 -*-

from flask import Blueprint, flash, render_template, session, request, jsonify

from fpage.models import Submission, Comment, db, User
from fpage.forms import CommentForm
from fpage.utils import flash_errors


blueprint = Blueprint('comments', __name__,
                      static_folder="../static",
                      template_folder="../templates")


@blueprint.route("/comments/<thread_id>", methods=['GET'])
def comments(thread_id):
    try:
        thread_id = int(thread_id)
        thread = Submission.query.filter_by(id=int(thread_id)).first()
        if thread is None:
            raise ValueError
    except ValueError:
        return render_template("404.html")

    # import pdb;pdb.set_trace()
    return render_template("comments.html",
                           post=thread,
                           comments=thread.get_comments())


@blueprint.route('/comment/post', methods=['POST'])
def post_comment():
    # import pdb;pdb.set_trace()
    if 'logged_in' not in session:
        return jsonify({"response": "You need to be log in to comment"})
    else:
        user = User.query.filter_by(username=session['username']).first()

    if user is None:
        return jsonify({"response":"Invalid user given"})

    if request.form['content']:
        comment_content=request.form['content']
    else:
        return jsonify({"response": "No comment content found"})

    parent_id=None if request.form['parent_id']=="root" else request.form['parent_id']

    try:
        thread_id = int(request.form['thread_id'])
        thread = Submission.query.filter_by(id=thread_id).first()
        if thread is None:
            return jsonify({"response": "Error posting comment: thread not found"})
    except:
        return jsonify({"response": "Error while posting comment: invalid thread id"})

    if thread.post_comment(user, comment_content, parent_id):
        return jsonify({"response": "Comment posted successfully"})
    else:
        return jsonify({"response": "Error posting comment"})



    return jsonify({"response": "If you can read this something went wrong. No idea what."})
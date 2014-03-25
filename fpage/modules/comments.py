# -*- coding: utf-8 -*-

import datetime

from flask import Blueprint, render_template, session, request, jsonify

from fpage.models import Submission, User

NESTED_LIMIT = 5

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

    return render_template("comments.html",
                           post=thread,
                           comments=thread.get_comments(),
                           n_limit=NESTED_LIMIT)


@blueprint.route('/comment/post', methods=['POST'])
def post_comment():
    if 'logged_in' not in session:
        return jsonify({"response": "You need to be log in to comment"})
    else:
        user = User.query.filter_by(username=session['username']).first()

    if user is None:
        return jsonify({"response": "Invalid user given"})

    if request.form['content']:
        comment_content = request.form['content']
    else:
        return jsonify({"response": "No comment content found"})

    if len(comment_content) > 5000:
        return jsonify({"response": "Comment over 5000 characters"})
    elif len(comment_content) < 1:
        return jsonify({"response": "No comment content"})

    parent_id = None if request.form['parent_id'] == "root" else request.form['parent_id']

    try:
        thread_id = int(request.form['thread_id'])
        thread = Submission.query.filter_by(id=thread_id).first()
        if thread is None:
            return jsonify({"response": "Error posting comment: thread not found"})
    except:
        return jsonify({"response": "Error while posting comment: invalid thread id"})
    timestamp = datetime.datetime.now()
    post_response = thread.post_comment(user, comment_content, NESTED_LIMIT, timestamp, parent_id)
    if post_response is True:
        return jsonify({"response": "Comment posted successfully"})
    elif post_response:  # recieved text response
        return jsonify({"response": post_response})
    else:
        return jsonify({"response": "Error posting comment"})

    return jsonify({"response": "If you can read this something went wrong. No idea what."})
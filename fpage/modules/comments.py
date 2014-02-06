# -*- coding: utf-8 -*-

from flask import Blueprint, flash, render_template, session, request, jsonify

from fpage.models import Submission, Comment, db
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

    form = CommentForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        if 'logged_in' not in session:
            flash('You need to be logged in to post comments', 'warning')
        else:
            new_comment = Comment(thread_id=thread_id,
                                  author=session['username'],
                                  content=form.content.data)
            try:
                thread.comment_count += 1
                db.session.add(new_comment)
                db.session.commit()
                form.content.data = ""
            except:
                flash("Error encountered while trying to post comment", 'warning')
    else:
        flash_errors(form)

    return render_template("comments.html",
                           post=thread,
                           comments=Comment.query.filter_by(thread_id=thread_id),
                           form=form)


@blueprint.route('/comment/post', methods=['POST'])
def post_comment():
    try:
        thread_id = int(request.form['thread_id'])
        thread = Submission.query.filter_by(id=thread_id).first()
        if thread is None:
            raise ValueError
    except:
        return jsonify({"response": "Error while posting comment"})
    form = CommentForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        if 'logged_in' not in session:
            return jsonify({"response": 'You need to be logged in to post comments'})
        else:
            new_comment = Comment(thread_id=thread_id,
                                  author=session['username'],
                                  content=form.content.data)
            try:
                thread.comment_count += 1
                db.session.add(new_comment)
                db.session.commit()
                form.content.data = ""
            except:
                return jsonify({"response": "Error encountered while trying to post comment"})
    else:
        return jsonify({"response": "Comment must contain between 1 and 5000 characters"})
    return jsonify({"response": "Comment posted successfully"})
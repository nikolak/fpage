# -*- coding: utf-8 -*-
from flask import Blueprint, session, request, jsonify

import fpage.comment
from fpage.extensions import db
import fpage.user
import fpage.submission
from .models import CommentVotes, ThreadVotes


blueprint = Blueprint("votes", __name__,
                      static_folder="../static")


@blueprint.route("/vote", methods=['POST'])
def vote():
    user_name = session['username']
    obj_id = request.form['object_id']
    direction = request.form['direction']
    vote_type = request.form['vote_type']
    response = {"data": None}

    if user_name is None:
        return jsonify({"data": "Not logged in"})

    user = fpage.user.models.User.query.filter_by(username=user_name).first()

    if user is None:
        return jsonify({"data": "Invalid username"})

    try:
        obj_id = int(obj_id)
    except:
        return jsonify({"data": "Invalid object id"})

    if vote_type == "comment":
        vote_object = fpage.comment.models.Comment.query.filter_by(id=obj_id).first()
    elif vote_type == "submission":
        vote_object = fpage.submission.models.Submission.query.filter_by(id=obj_id).first()
    else:
        return jsonify({"data": "no vote type passed"})

    if vote_object is None:
        return jsonify({"data": "Sub not found"})

    if direction not in ['up', 'down']:
        return jsonify({"data": "invalid vote direction"})

    direction_value = 1 if direction == "up" else -1

    if vote_type == "comment":
        vote = CommentVotes.query.filter_by(comment_id=vote_object.id).first()
    else:
        vote = ThreadVotes.query.filter_by(thread_id=vote_object.id).first()

    if vote is None:  # first time voting on this

        if vote_type == "comment":
            new_vote = CommentVotes(user, vote_object, direction_value)
        else:
            new_vote = ThreadVotes(user, vote_object, direction_value)
        db.session.add(new_vote)
        if direction == "up":
            vote_object.ups += 1
        else:
            vote_object.downs += 1
        response = {"data": "upvoted" if direction == "up" else "downvoted"}

    elif vote.vote_value == 0:  # re-upvoting/downvoting after removed vote
        vote.vote_value = direction_value
        if direction == "up":
            vote_object.ups += 1
        else:
            vote_object.downs += 1
        response = {"data": "upvoted" if direction == "up" else "downvoted"}

    elif vote.vote_value == direction_value:  #canceling the vote
        vote.vote_value = 0
        if direction == "up":
            vote_object.ups -= 1
        else:
            vote_object.downs -= 1
        response = {"data": "{}_cancel".format(direction)}

    elif vote.vote_value in [-1, 1] and vote.vote_value != direction_value:  # opposite vote
        if vote.vote_value == 1:  # changing from positive (upvote) to negative (downvote)
            vote.vote_value = -1
            response = {"data": "up_to_down"}
            vote_object.ups -= 1
            vote_object.downs += 1
        else:
            vote.vote_value = 1
            response = {"data": "down_to_up"}
            vote_object.ups += 1
            vote_object.downs -= 1

    db.session.commit()
    return jsonify(response)
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request, session
from fpage.utils import login_required
from fpage.models import Vote, Submission
from fpage.models import db

blueprint = Blueprint('vote', __name__,
                      static_folder="../static",
                      template_folder="../templates")


@blueprint.route("/vote", methods=['POST'])
@login_required
def vote():
    user = session['username']
    sub_id=request.form['submission']
    direction=request.form['direction']
    response={"data":None}

    if user is None:
        return jsonify({"data":"Not logged in"})

    try:
        sub_id=int(sub_id)
    except:
        return jsonify({"data":"Invalid sub id"})

    submission=Submission.query.filter_by(id=sub_id).first()

    if submission is None:
        return jsonify({"data":"Sub not found"})

    if direction not in ['up', 'down']:
        return jsonify({"data":"invalid vote direction"})

    direction_value=1 if direction=="up" else -1

    vote=Vote.query.filter_by(user=user, submission_id=sub_id).first()


    if vote is None: # first time voting on this
        new_vote=Vote(user=user, submission_id=sub_id, vote_value=direction_value)
        db.session.add(new_vote)
        if direction=="up":
            submission.ups+=1
        else:
            submission.downs+=1
        response = {"data": "upvoted" if direction == "up" else "downvoted"}

    elif vote.vote_value==0: # re-upvoting/downvoting after removed vote
        vote.vote_value=direction_value
        if direction=="up":
            submission.ups+=1
        else:
            submission.downs+=1
        response={"data":"upvoted" if direction=="up" else "downvoted"}

    elif vote.vote_value==direction_value: #canceling the vote
        vote.vote_value=0
        if direction=="up":
            submission.ups-=1
        else:
            submission.downs-=1
        response={"data":"{}_cancel".format(direction)}

    elif vote.vote_value in [-1,1] and vote.vote_value!=direction_value: # opposite vote
        if vote.vote_value==1: # changing from positive (upvote) to negative (downvote)
            vote.vote_value=-1
            response={"data":"up_to_down"}
            submission.ups-=1
            submission.downs+=1
        else:
            vote.vote_value=1
            response={"data":"down_to_up"}
            submission.ups+=1
            submission.downs-=1

    db.session.commit()
    return jsonify(response)
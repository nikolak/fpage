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
    sub_id = request.form['postId']
    try:
        vote = {"up": 1, "down": -1}[request.form['voteDir']]
        changing_vote = False
        if vote not in [-1, 1]:
            raise ValueError
        v = Vote.query.filter_by(user=user, submission_id=sub_id).first()
        if v is None:
            # first time voting
            new_vote = Vote(user=user, submission_id=sub_id, vote_value=vote)
            db.session.add(new_vote)
        elif v.vote_value != vote:
            # changing vote, we need bool to change value of other field
            # in submission, to avoid duplicate votes
            v.vote_value = vote
            changing_vote = True

        else:
            return jsonify({
                'new_value': request.form['cValue']})

        submission = Submission.query.filter_by(id=sub_id).first()
        if submission is None:
            raise Exception
        else:
            if vote == 1:
                submission.ups += 1
                if changing_vote and submission.downs > 0:
                    submission.downs -= 1
            elif vote == -1:
                submission.downs += 1
                if changing_vote and submission.ups > 0:
                    submission.ups -= 1
            else:
                raise Exception
        db.session.commit()

        new_value = " " + str(int(request.form['cValue']) + 1)

        if changing_vote:
            other_value = " " + str(int(request.form['otherValue']) - 1)
        else:
            other_value = request.form['otherValue']
    except:
        return jsonify({
            'new_value': request.form['cValue'],
            'other_value': request.form['otherValue']})

    return jsonify({
        'new_value': new_value,
        'other_value': other_value})
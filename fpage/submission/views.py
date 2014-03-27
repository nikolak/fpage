# -*- coding: utf-8 -*-
import datetime
from flask import Blueprint, render_template, flash, request, session
from fpage.utils import login_required
from werkzeug.utils import redirect
from fpage.extensions import db
from fpage.submission.forms import SubmitForm
from fpage.utils import flash_errors
import fpage.user

from .models import Submission
blueprint = Blueprint("submission", __name__,
                      static_folder="../static")

@blueprint.route("/", methods=['GET'])
@blueprint.route("/page/<page_id>", methods=['GET'])
def page(page_id=1):
    try:
        page_id = int(page_id)
    except ValueError:
        flash("Invalid page number", 'warning')
        page_id = 1
    return render_template("submissions/submissions.html",
                           posts=Submission.query.order_by(Submission.ups.desc())[(page_id * 25) - 25:page_id * 25],
                           page=int(page_id))


    #
    # Score = Lower bound of Wilson score confidence interval for a Bernoulli parameter
    #
    # http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
    #
@blueprint.route("/submit/", methods=["GET", "POST"])
@login_required
def submit():
    form = SubmitForm(request.form, csrf_enabled=False)

    if form.validate_on_submit():
        user = fpage.user.models.User.query.filter_by(username=session['username']).first()
        if user is None:
            flash("Error getting user", 'warning')
        else:
            new_submission = Submission(title=form.title.data,
                                        url=form.url.data,
                                        timestamp=datetime.datetime.now(),
                                        author=user.username)
            try:
                db.session.add(new_submission)
                db.session.commit()
                return redirect('/comments/{}'.format(new_submission.id))
            except:
                flash("Error encountered while trying to post submission", 'warning')
    else:
        flash_errors(form)
    return render_template("submissions/submit_page.html", form=form)
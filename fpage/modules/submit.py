# -*- coding: utf-8 -*-

import datetime

from flask import Blueprint, render_template, request, flash, session, redirect

from fpage.utils import login_required
from fpage.models import db, Submission, User
from fpage.forms import SubmitForm
from fpage.utils import flash_errors


blueprint = Blueprint('submit', __name__,
                      static_folder="../static",
                      template_folder="../templates")


@blueprint.route("/submit/", methods=["GET", "POST"])
@login_required
def submit():
    form = SubmitForm(request.form, csrf_enabled=False)

    if form.validate_on_submit():
        user = User.query.filter_by(username=session['username']).first()
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
    return render_template("submit.html", form=form)
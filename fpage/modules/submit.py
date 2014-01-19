# -*- coding: utf-8 -*-
'''Members-only module, typically including the app itself.
'''
from flask import Blueprint, render_template, request, flash, session
import time

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
        # print user
        if user is None:
            flash("Error getting user", 'warning')
        else:
            # print form.title.data,form.url.data,user
            new_submission = Submission(title=form.title.data,
                                        url=form.url.data,
                                        timestamp=int(time.time()),
                                        author=user)
            try:
                db.session.add(new_submission)
                db.session.commit()
                flash("Successfully created new thread", 'success')
            except:
                flash("Error encountered while trying to post submission", 'warning')
    else:
        flash_errors(form)
    return render_template("submit.html", form=form)
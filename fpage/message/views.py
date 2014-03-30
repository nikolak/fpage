# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session
from fpage.utils import login_required

import models
import fpage.user.models
blueprint = Blueprint("message", __name__, url_prefix='/inbox',
                      static_folder="../static")


@blueprint.route("/")
@login_required
def main():
    messages=models.Message.query.filter_by(reciever=session['username']).order_by(models.Message.id.desc()).all()
    user=fpage.user.models.User.query.filter_by(username=session['username']).first()
    user.update(unread_count=0)
    session['unread']=0
    return render_template("messages/inbox.html", messages=messages)
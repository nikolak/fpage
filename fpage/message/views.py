# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session

from fpage.utils import login_required
import models
import fpage.user.models


blueprint = Blueprint("message", __name__, url_prefix='/inbox',
                      static_folder="../static")


@blueprint.route("/")
@blueprint.route("/<int:page_id>")
@login_required
def main(page_id=1):
    messages = models.Message.query.filter_by(reciever=session['username']).order_by(models.Message.id.desc()).all()[
               (page_id * 25) - 25:page_id * 25]
    user = fpage.user.models.User.query.filter_by(username=session['username']).first()

    user.update(unread_count=0)
    session['unread'] = 0

    return render_template("messages/inbox.html",
                           messages=messages,
                           page=page_id)
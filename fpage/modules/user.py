# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

from fpage.models import User


blueprint = Blueprint('user', __name__,
                      static_folder="../static",
                      template_folder="../templates")


@blueprint.route("/user/<username>", methods=['GET'])
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return render_template("404.html")
    else:
        return render_template("user.html",
                               user=user)
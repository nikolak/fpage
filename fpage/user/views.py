# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
import fpage.user

blueprint = Blueprint("user", __name__, url_prefix='/user',
                        static_folder="../static")


@blueprint.route("/<username>", methods=['GET'])
def user(username):
    user = fpage.user.models.User.query.filter_by(username=username).first()
    if user is None:
        return render_template("404.html")
    else:
        return render_template("users/user.html",
                               user=user)
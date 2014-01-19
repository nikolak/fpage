# -*- coding: utf-8 -*-

from flask import Blueprint, flash, render_template
from fpage.models import Submission

blueprint = Blueprint('page', __name__,
                      static_folder="../static",
                      template_folder="../templates")


@blueprint.route("/", methods=['GET'])
@blueprint.route('/page/<id>', methods=['GET'])
def page(id=1):
    try:
        id = int(id)
    except ValueError:
        flash("Invalid page number", 'warning')
        id = 1
    return render_template("page.html",
                           posts=Submission.query.order_by(Submission.ups.desc())[(id * 25) - 25:id * 25],
                           page=int(id))


    #
    # Score = Lower bound of Wilson score confidence interval for a Bernoulli parameter
    #
    # http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
    #
# -*- coding: utf-8 -*-

from flask import Blueprint, flash, render_template

from fpage.models import Submission


blueprint = Blueprint('page', __name__,
                      static_folder="../static",
                      template_folder="../templates")


@blueprint.route("/", methods=['GET'])
@blueprint.route('/page/<page_id>', methods=['GET'])
def page(page_id=1):
    try:
        page_id = int(page_id)
    except ValueError:
        flash("Invalid page number", 'warning')
        page_id = 1
    return render_template("page.html",
                           posts=Submission.query.order_by(Submission.ups.desc())[(page_id * 25) - 25:page_id * 25],
                           page=int(page_id))


    #
    # Score = Lower bound of Wilson score confidence interval for a Bernoulli parameter
    #
    # http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
    #
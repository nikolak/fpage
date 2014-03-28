# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session, url_for, flash, request, jsonify
from werkzeug.utils import redirect

from fpage.utils import login_required
import fpage.user.models
import fpage.comment.models
import fpage.submission.models


blueprint = Blueprint("admin", __name__, url_prefix='/admin',
                      static_folder="../static")


@blueprint.route("/")
@login_required
def main():
    admin = fpage.user.models.User.query.filter_by(is_admin=True).first()

    if admin:
        if admin.username != session['username']:
            return redirect(url_for('submission.page'))
        else:
            return redirect(url_for('submission.page'))
    else:
        user = fpage.user.models.User.query.filter_by(username=session['username']).first()
        user.update(is_admin=True)
        flash('Added as admin', 'success')
        return render_template('submission.page')


@blueprint.route('/remove', methods=['POST'])
@login_required
def remove():
    admin_user = fpage.user.models.User.query.filter_by(is_admin=True,
                                                        username=session['username']).first()

    if not admin_user:
        return jsonify({"data": "error"})

    object_type = request.form['object_type']
    object_id = request.form['object_id']

    try:
        object_id = int(object_id)
    except:
        return jsonify({"data": "error"})

    # TODO: Check that these objects really exist before trying to remove them
    if object_type == 'comment':
        comment = fpage.comment.models.Comment.query.filter_by(id=object_id).first()
        comment.delete()
        return jsonify({"data": "removed"})
    elif object_type == 'submission':
        submission = fpage.submission.models.Submission.query.filter_by(id=object_id).first()
        submission.delete()
        return jsonify({"data": "removed"})
    elif object_type == 'user':
        user = fpage.user.models.User.query.filter_by(id=object_id).first()
        user.delete()
        return jsonify({"data": "removed"})
    else:
        return jsonify({"data": "unknown"})
